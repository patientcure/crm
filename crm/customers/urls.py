# customers/urls.py
from django.urls import path
from .views import CustomerViewSet, CommissionSummaryAPIView

urlpatterns = [
    # --- Commission Summary API (Admin Only) ---
    # GET: Retrieve the commission summary report
    path(
        'commissions/summary/', 
        CommissionSummaryAPIView.as_view(), 
        name='commission-summary'
    ),
    
    # --- Customer CRUD API (List and Create) ---
    # GET: List all customers (filtered by role in ViewSet)
    # POST: Create a new customer (Admin only via this endpoint, public endpoint is separate)
    path(
        'management/', 
        CustomerViewSet.as_view({'get': 'list', 'post': 'create'}), 
        name='customer-management-list-create'
    ),
    
    # --- Customer CRUD API (Retrieve, Update, Delete) ---
    # GET: Retrieve a specific customer
    # PUT/PATCH: Update a specific customer
    # DELETE: Delete a specific customer (Admin only)
    path(
        'management/<int:pk>/', 
        CustomerViewSet.as_view({
            'get': 'retrieve', 
            'put': 'update', 
            'patch': 'partial_update', 
            'delete': 'destroy'
        }), 
        name='customer-management-detail'
    ),
]