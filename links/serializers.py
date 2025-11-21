# links/serializers.py (UPDATED)
from rest_framework import serializers
from .models import Link, Bank, Product
from django.urls import reverse
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
            'description',
            'image',
            'unique_customer_link',
        )
        read_only_fields = ('id', 'unique_customer_link', 'bank_name', 'product_name')
        

    def get_unique_customer_link(self, obj):
            request = self.context.get('request')
            if not request or not request.user.is_authenticated:
                return None

            user = request.user
            # 2. GET THE USER'S ROLE, default to empty string if not present
            user_role = getattr(user, 'role', '').upper()

            # 3. USE YOUR SUGGESTED LOGIC
            if user_role in ('CONNECTOR', 'STAFF', 'ADMIN'):
                
                # 4. IMPLEMENT "OPTION 2" to build the URL
                try:
                    # This 'name' MUST match the one in urls.py (Step 2)
                    path = reverse('customer_onboarding_track', kwargs={'link_id': obj.id, 'connector_id': user.id})
                    return request.build_absolute_uri(path)
                except Exception as e:
                    # This helps you debug if the URL name is missing or wrong
                    return f"Error: URL 'customer_onboarding_track' not configured. {e}"

            # Returns None if the user role is not one of the above
            return None
        
    def validate(self, data):
        """
        Ensure bank+product pair is unique.
        When updating, allow the same instance to keep its bank/product.
        """
        request = self.context.get('request', None)
        bank = data.get('bank', getattr(self.instance, 'bank', None))
        product = data.get('product', getattr(self.instance, 'product', None))

        if not bank or not product:
            # Let field-level validation handle missing FKs
            return data

        qs = Link.objects.filter(bank=bank, product=product)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise serializers.ValidationError({
                'non_field_errors': ["A Link for this bank and product already exists. "
                                     "Modify or delete that one instead of creating a new one."]
            })
        return data