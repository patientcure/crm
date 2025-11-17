# links/views.py (UPDATED)
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Link, Bank, Product
from .serializers import LinkSerializer, BankSerializer, ProductSerializer
from .permissions import IsAdminOrReadOnly
from django.db import IntegrityError, transaction
from rest_framework import status
from rest_framework.response import Response

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
    queryset = Link.objects.all().order_by('bank__name', 'product__name')
    serializer_class = LinkSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    def get_serializer_context(self):
        return {'request': self.request}

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            with transaction.atomic():
                self.perform_create(serializer)
        except IntegrityError:
            return Response(
                {"detail": "A Link for this bank and product already exists."},
                status=status.HTTP_400_BAD_REQUEST
            )
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)