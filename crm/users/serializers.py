# users/serializers.py
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'phone', 'username', 'email', 'first_name', 'last_name', 'role', 'is_active', 'is_staff')
        read_only_fields = ('id', 'is_active', 'is_staff')

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Simple phone/password login - now phone IS the username
    """
    phone = serializers.CharField()
    password = serializers.CharField()
    
    def validate(self, attrs):
        phone = attrs.get('phone')
        password = attrs.get('password')
        
        # Authenticate using phone (which is the USERNAME_FIELD)
        user = authenticate(username=phone, password=password)
        if not user:
            raise serializers.ValidationError('Invalid phone number or password')
        
        if not user.is_active:
            raise serializers.ValidationError('User account is disabled')
        
        # Generate token
        refresh = self.get_token(user)
        
        # Add custom claims
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
        
        # Generate username from phone (you can modify this logic as needed)
        phone = validated_data['phone']
        username = f"user_{phone}"  # or just use phone as username
        
        user = User.objects.create_user(
            username=username,  # Set username automatically
            password=password,
            **validated_data
        )
        return user