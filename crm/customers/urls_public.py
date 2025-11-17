# customers/urls_public.py
from django.urls import path
from .views_public import CustomerOnboardingAPIView

urlpatterns = [
        path(
        'customer/<int:link_id>/<int:connector_id>/',
        CustomerOnboardingAPIView.as_view(),
        name='customer_onboarding_track'
    ),
]