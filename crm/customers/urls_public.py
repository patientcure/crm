# customers/urls_public.py
from django.urls import path
from .views_public import CustomerOnboardingAPIView

urlpatterns = [
    # Endpoint for customer form submission and tracking
    # Example: /onboard/123/?ref=456
    path('<int:link_id>/', CustomerOnboardingAPIView.as_view(), name='customer_onboarding_base'),
]