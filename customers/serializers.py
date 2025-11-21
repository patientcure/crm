# customers/serializers.py
from rest_framework import serializers
from .models import Customer, User, Link

class CustomerOnboardingSerializer(serializers.ModelSerializer):
    """
    Serializer for public customer data submission.
    """
    class Meta:
        model = Customer
        fields = ('name', 'phone', 'email', 'pan')
        

class CustomerAdminSerializer(CustomerOnboardingSerializer):
    """
    Extended serializer for Admin/Staff access, showing commission and referral details.
    """
    referred_by_name = serializers.CharField(source='referred_by.name', read_only=True)
    referred_by_phone = serializers.CharField(source='referred_by.phone', read_only=True)
    product_name = serializers.CharField(source='referred_for_product.name', read_only=True)
    
    class Meta:
        model = Customer
        fields = (
            'id', 'name', 'phone', 'email', 'pan', 
            'referred_by', 'referred_by_name', 'referred_by_phone', 
            'referred_for_product', 'product_name', 
            'commission_amount', 'created_at', 'status', 'description'
        )
        read_only_fields = ('referred_by_name', 'referred_by_phone', 'product_name', 'created_at')