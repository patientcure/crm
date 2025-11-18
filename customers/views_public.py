# customers/views_public.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404, redirect
from users.models import User
from links.models import Link
from .models import Customer
from .serializers import CustomerOnboardingSerializer

class CustomerOnboardingAPIView(APIView):
    """
    Public endpoint for customer data submission and tracking redirect.
    URL: /onboard/<link_id>/<connector_id>/
    """
    permission_classes = () # Public access

    def get(self, request, link_id, connector_id, format=None):
        """
        Handles GET: Return details about the link and the connector.
        """
        link = get_object_or_404(Link, pk=link_id)
        
        try:
            connector = User.objects.get(id=connector_id)
            if connector.role not in ('ADMIN', 'STAFF', 'CONNECTOR'):
                 return Response(
                    {"detail": "The specified connector is not valid."},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except User.DoesNotExist:
             return Response(
                {"detail": "The specified connector is not valid."},
                status=status.HTTP_404_NOT_FOUND
            )

        # Return the details
        return Response({
            "link_details": {
                "id": link.id,
                "bank_name": link.bank.name,
                "product_name": link.product.name,
                "utm_link": link.utm_link
            },
            "user_details": {
                "id": connector.id,
                "name": connector.get_full_name() or connector.username,
                "role": connector.role
            }
        })

    def post(self, request, link_id, connector_id, format=None):
        """
        Handles POST: Creates a new customer record.
        """
        serializer = CustomerOnboardingSerializer(data=request.data)
        
        if serializer.is_valid():
            # 1. Identify the referring user and product
            # The ID now comes from the URL, not query_params
            try:
                referrer_user = User.objects.get(id=connector_id)
                if referrer_user.role not in ('STAFF', 'CONNECTOR'):
                    return Response(
                        {"detail": "Invalid connector."},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            except User.DoesNotExist:
                return Response(
                    {"detail": "Invalid connector."},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            link = get_object_or_404(Link, id=link_id)

            # 2. Check for duplicate PAN
            pan = serializer.validated_data['pan']
            if Customer.objects.filter(pan=pan).exists():
                return Response(
                    {'pan': ['A customer with this PAN already exists.']}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            # 3. Create the Customer record
            customer = serializer.save(
                referred_by=referrer_user,
                referred_for_product=link
            )

            # 4. Success response and redirection instructions
            return Response({
                "message": "Customer saved successfully.",
                "redirect_url": link.utm_link
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)