# users/views.py
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import User
from .serializers import UserRegistrationSerializer, UserSerializer
from .permissions import IsAdminUser

class UserRegistrationAPIView(generics.CreateAPIView):
    """
    User registration - Only admins can create users
    """
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
                "role": user.role
            }
        }, status=status.HTTP_201_CREATED)

class UserProfileAPIView(generics.RetrieveAPIView):
    """
    Get current user profile
    """
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        return self.request.user