# customers/views.py
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum
from .models import Customer
from .serializers import CustomerAdminSerializer
from .permissions import IsAdminOrOwnCustomer
from users.permissions import IsAdminUser

class CustomerViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Admin/Staff/Connector to view and manage customer records.
    Admin can edit commission_amount and all fields.
    Staff/Connector can view only their referred customers and edit basic details (Name, Phone, Email, Pan).
    """
    serializer_class = CustomerAdminSerializer
    permission_classes = [IsAuthenticated, IsAdminOrOwnCustomer]
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'ADMIN':
            return Customer.objects.all().order_by('-created_at')
        
        # Staff/Connector can only see customers they referred
        return Customer.objects.filter(referred_by=user).order_by('-created_at')

    def perform_update(self, serializer):
        # Admin can update everything, including commission.
        # Staff/Connector can only update basic customer fields.
        if not self.request.user.is_admin:
            # Prevent Staff/Connector from updating commission field via API
            if 'commission_amount' in serializer.validated_data:
                del serializer.validated_data['commission_amount']

        serializer.save()


class CommissionSummaryAPIView(APIView):
    """
    API endpoint for Admin to view total commissions of each connector.
    """
    permission_classes = [IsAuthenticated, IsAdminUser] # Only Admin access

    def get(self, request, format=None):
        commission_summary = Customer.objects.values(
            'referred_by__id', 
            'referred_by__phone', 
            'referred_by__name',
            'referred_by__role'
        ).annotate(
            total_commission=Sum('commission_amount')
        ).filter(
            referred_by__isnull=False,
            referred_by__role__in=['STAFF', 'CONNECTOR']
        ).order_by('-total_commission')

        # Convert queryset results to a list for JSON response
        return Response(list(commission_summary))