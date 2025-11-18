from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView
)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # --- API Documentation Endpoints ---
    # 1. Generate the OpenAPI schema (JSON/YAML)
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    
    # 2. Swagger UI: Interactive documentation interface
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    
    # 3. Redoc UI: Alternative documentation interface (often preferred for reading)
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    
    # --- Application Endpoints ---
    path('api/', include('users.urls')),          # Auth APIs
    path('api/links/', include('links.urls')),    # Link Mgmt APIs
    path('api/customers/', include('customers.urls')), # Customer Mgmt APIs
    
    # Public tracking endpoint
    path('onboard/', include('customers.urls_public')), 
]