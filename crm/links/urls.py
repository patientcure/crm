# links/urls.py
from django.urls import path
from links.views import BankViewSet, ProductViewSet, LinkViewSet

urlpatterns = [
    # --- Bank Management API (Admin CRUD) ---
    # GET: List all Banks
    # POST: Create a new Bank
    path(
        'banks/', 
        BankViewSet.as_view({'get': 'list', 'post': 'create'}), 
        name='bank-list-create'
    ),
    # GET: Retrieve a specific Bank
    # PUT/PATCH: Update a specific Bank
    # DELETE: Delete a specific Bank
    path(
        'banks/<int:pk>/', 
        BankViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), 
        name='bank-detail'
    ),
    
    # --- Product Type Management API (Admin CRUD) ---
    # GET: List all Products
    # POST: Create a new Product
    path(
        'products/types/', 
        ProductViewSet.as_view({'get': 'list', 'post': 'create'}), 
        name='product-type-list-create'
    ),
    # GET: Retrieve a specific Product
    # PUT/PATCH: Update a specific Product
    # DELETE: Delete a specific Product
    path(
        'products/types/<int:pk>/', 
        ProductViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), 
        name='product-type-detail'
    ),
    
    # --- Main Links API (Admin CRUD, Others Read-Only) ---
    # GET: List all Links
    # POST: Create a new Link
    path(
        'products/links/', 
        LinkViewSet.as_view({'get': 'list', 'post': 'create'}), 
        name='link-product-entry-list-create'
    ),
    # GET: Retrieve a specific Link (and get unique_customer_link)
    # PUT/PATCH: Update a specific Link
    # DELETE: Delete a specific Link
    path(
        'products/links/<int:pk>/', 
        LinkViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), 
        name='link-product-entry-detail'
    ),
]