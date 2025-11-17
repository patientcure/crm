# mycrm_project/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('users.urls')),       # Core authentication routes
    # Other app APIs will go under /api/
    path('api/links/', include('links.urls')), 
    path('api/customers/', include('customers.urls')),
    
    # Customer Onboarding view (still needs to be outside /api/ as it's for public clicks)
    path('onboard/', include('customers.urls_public')), 
]