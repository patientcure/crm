# users/views.py
from rest_framework import generics, status,viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import User, TermsAndConditions, HomePageSlider
from .serializers import (
    UserRegistrationSerializer, 
    UserSerializer, 
    UserDetailSerializer,
    TermsAndConditionsSerializer,
    HomePageSliderSerializer
)
from .permissions import IsAdminUser
from customers.models import Customer
from links.models import Product
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import uuid
import json

class UserRegistrationAPIView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        return Response({
            "message": f"User {user.phone} ({user.role}) created successfully",
            "user": {
                "id": user.id,
                "phone": user.phone,
                "first_name": user.first_name,
                "role": user.role,
                "created_at": user.created_at
            }
        }, status=status.HTTP_201_CREATED)

class UserProfileAPIView(generics.RetrieveAPIView):
    """
    Get current user profile (Self)
    Uses standard serializer (no customer list needed usually for self profile unless requested)
    """
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        return self.request.user

class UserListAPIView(generics.ListAPIView):
    queryset = User.objects.all().prefetch_related('products')  # add prefetch
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]


class UserDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    Admin View: Retrieve single user with FULL details (including referred customers).
    """
    # Use the serializer that includes 'referred_customers'
    serializer_class = UserDetailSerializer 
    permission_classes = [IsAuthenticated, IsAdminUser]
    lookup_field = "pk"

    def get_queryset(self):
        """
        Optimize query to fetch customers, banks, and products efficiently.
        """
        return User.objects.prefetch_related(
            'products',
            'customer_set', 
            'customer_set__referred_for_product',
            'customer_set__referred_for_product__bank',
            'customer_set__referred_for_product__product'
        )

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", True)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(
            {"message": f"User {instance.phone} updated successfully.", "user": serializer.data},
            status=status.HTTP_200_OK,
        )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        phone = getattr(instance, "phone", str(instance.pk))
        self.perform_destroy(instance)
        return Response({"message": f"User {phone} deleted successfully."}, status=status.HTTP_200_OK)
    
class TermsAndConditionsAPIView(generics.RetrieveUpdateAPIView):
    queryset = TermsAndConditions.objects.all()
    serializer_class = TermsAndConditionsSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH']:
            self.permission_classes.append(IsAdminUser)
        return super().get_permissions()

    def get_object(self):
        return self.queryset.first()

class HomePageStatsAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = HomePageSliderSerializer
    pagination_class = None

    def get_queryset(self):
        return HomePageSlider.objects.filter(is_active=True).order_by('order')

    def list(self, request, *args, **kwargs):
        # Get the sliders using the serializer
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        
        # Calculate Stats
        live_stats = {
            "total_customers": Customer.objects.count(),
            "total_staff": User.objects.filter(role='STAFF').count(),
            "total_connectors": User.objects.filter(role='CONNECTOR').count(),
            "total_admins": User.objects.filter(role='ADMIN').count(),
            "total_products": Product.objects.count(),
        }

        return Response({
            "sliders": serializer.data,
            "live_stats": live_stats
        })

class HomePageSliderViewSet(viewsets.ModelViewSet):
    queryset = HomePageSlider.objects.all()
    serializer_class = HomePageSliderSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]