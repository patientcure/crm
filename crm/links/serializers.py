# links/serializers.py (UPDATED)
from rest_framework import serializers
from .models import Link, Bank, Product
# ... (User import is not needed here) ...

# --- New Serializers ---
class BankSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bank
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

# --- Link Serializer Update ---
class LinkSerializer(serializers.ModelSerializer):
    """
    Serializer for Link model, now using Bank and Product foreign keys.
    """
    unique_customer_link = serializers.SerializerMethodField(read_only=True)
    # Read-only fields to show the Bank/Product name in the Link list view
    bank_name = serializers.CharField(source='bank.name', read_only=True)
    product_name = serializers.CharField(source='product.name', read_only=True)
    
    class Meta:
        model = Link
        fields = (
            'id', 
            'bank',         # Writable FK for Admin to set (dropdown)
            'bank_name',    # Read-only name for display
            'product',      # Writable FK for Admin to set (dropdown)
            'product_name', # Read-only name for display
            'name', 
            'user_id', 
            'password', 
            'utm_link', 
            'image',
            'unique_customer_link',
        )
        read_only_fields = ('id', 'unique_customer_link', 'bank_name', 'product_name')
        
    def get_unique_customer_link(self, obj):
        # ... (Logic remains the same, assuming we pass the request in context) ...
        request = self.context.get('request')
        
        if request and request.user.is_authenticated and request.user.is_connector_or_staff:
            return obj.get_connector_unique_link(request.user)
        return None