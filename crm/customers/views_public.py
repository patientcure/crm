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
    URL: /onboard/<link_id>/
    Query Params: ?ref=<user_id> (Only present on the initial tracked click)
    """
    permission_classes = () # Public access

    def post(self, request, link_id, format=None):
        serializer = CustomerOnboardingSerializer(data=request.data)
        
        if serializer.is_valid():
            # 1. Identify the referring user and product
            referrer_id = request.query_params.get('ref')
            
            referrer_user = None
            if referrer_id:
                try:
                    referrer_user = User.objects.get(id=referrer_id)
                except User.DoesNotExist:
                    # Log error, but proceed with un-referred customer
                    pass
            
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