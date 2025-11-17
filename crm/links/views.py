# links/views.py (UPDATED)
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Link, Bank, Product
from .serializers import LinkSerializer, BankSerializer, ProductSerializer
from .permissions import IsAdminOrReadOnly

# --- New ViewSets for Bank and Product Management ---

class BankViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing Banks (Admin CRUD, Others Read-Only).
    """
    queryset = Bank.objects.all()
    serializer_class = BankSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    # Admin can create and delete banks.

class ProductViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing Products (Admin CRUD, Others Read-Only).
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    # Admin can create and delete products.

# --- LinkViewSet remains the same ---
class LinkViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows links to be viewed, created, edited, or deleted.
    """
    queryset = Link.objects.all().order_by('bank__name', 'product__name')
    serializer_class = LinkSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    
    def get_serializer_context(self):
        return {'request': self.request}