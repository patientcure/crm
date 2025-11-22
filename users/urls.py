# users/urls.py
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenBlacklistView
from .views import UserRegistrationAPIView, UserProfileAPIView, UserListAPIView, UserDetailAPIView,TermsAndConditionsAPIView, HomePageAPIView
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer

urlpatterns = [
    # Authentication - Login with phone/password
    path('auth/login/', TokenObtainPairView.as_view(serializer_class=CustomTokenObtainPairSerializer), name='login'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/logout/', TokenBlacklistView.as_view(), name='logout'),
    
    # Registration - Only admins can access
    path('auth/register/', UserRegistrationAPIView.as_view(), name='register'),
    
    # Profile - Any authenticated user can access
    path('auth/profile/', UserProfileAPIView.as_view(), name='profile'),
    # User List Management Create Update Delete Modify - Only admins can access 
    path("users/", UserListAPIView.as_view(), name="user-list"),
    path("user/<int:pk>/", UserDetailAPIView.as_view(), name="user-detail"),
    path("terms/",TermsAndConditionsAPIView.as_view(), name="terms"),
    path("homepage/", HomePageAPIView.as_view(), name="homepage"),
]