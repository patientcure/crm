# users/serializers.py
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate
from .models import User, TermsAndConditions
from customers.models import Customer
from links.models import Product  # new import

# small helper serializer for product + access flag
class ProductAccessSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    has_access = serializers.BooleanField()

class UserSerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id', 'phone', 'username', 'email', 'first_name', 'last_name', 
            'role', 'is_active', 'is_staff', 'last_login', 'created_at', 'products'
        )
        read_only_fields = ('id', 'is_active', 'is_staff', 'last_login', 'created_at')

    def get_products(self, obj):
        all_products = Product.objects.all()
        user_products = set(obj.products.all().values_list('id', flat=True))
        result = []
        for p in all_products:
            result.append({
                'id': p.id,
                'name': getattr(p, 'name', '') if hasattr(p, 'name') else str(p),
                'has_access': p.id in user_products
            })
        return ProductAccessSerializer(result, many=True).data

# --- 2. New Serializer for the Customer List (Nested) ---
class CustomerReferralSerializer(serializers.ModelSerializer):
    """
    Used inside UserDetailSerializer to show customers referred by this user.
    Flattens the relationship to show Bank/Product names directly.
    """
    product_name = serializers.CharField(source='referred_for_product.product.name', read_only=True, default="N/A")
    bank_name = serializers.CharField(source='referred_for_product.bank.name', read_only=True, default="N/A")
    
    class Meta:
        model = Customer
        fields = (
            'id', 'name', 'phone', 'pan', 'status', 
            'commission_amount', 'created_at', 
            'product_name', 'bank_name'
        )

# --- 3. User Detail Serializer (Includes Customers) ---
class UserDetailSerializer(UserSerializer):
    """
    Extends UserSerializer to include the list of referred customers.
    Only used in Retrieve/Detail views to avoid overhead in List views.
    """
    # 'customer_set' is the default reverse related name for the ForeignKey in Customer model
    referred_customers = CustomerReferralSerializer(source='customer_set', many=True, read_only=True)

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ('referred_customers',)

# --- 4. Login Serializer (Updated) ---
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    phone = serializers.CharField()
    password = serializers.CharField()
    
    def validate(self, attrs):
        phone = attrs.get('phone')
        password = attrs.get('password')
        
        user = authenticate(username=phone, password=password)
        if not user:
            raise serializers.ValidationError('Invalid phone number or password')
        
        if not user.is_active:
            raise serializers.ValidationError('User account is disabled')
        
        refresh = self.get_token(user)
        refresh['phone'] = user.phone
        refresh['role'] = user.role
        
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': {
                'id': user.id,
                'phone': user.phone,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'last_login': user.last_login,
                'created_at': user.created_at,
                'role': user.role
            }
        }

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, style={'input_type': 'password'})
    
    class Meta:
        model = User
        fields = ('phone', 'first_name', 'last_name', 'email', 'role', 'password', 'password2')
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Passwords don't match"})
        if User.objects.filter(phone=attrs['phone']).exists():
            raise serializers.ValidationError({"phone": "User with this phone already exists"})
        if attrs.get('role') == 'ADMIN':
            raise serializers.ValidationError({"role": "Cannot create admin users via this endpoint"})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        password = validated_data.pop('password')
        phone = validated_data['phone']
        username = f"user_{phone}" 
        
        user = User.objects.create_user(
            username=username, 
            password=password, 
            **validated_data
        )
        return user
    

class TermsAndConditionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TermsAndConditions
        fields = ('content', 'updated_at', 'updated_by')