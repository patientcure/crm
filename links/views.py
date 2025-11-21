from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Link, Bank, Product
from .serializers import LinkSerializer, BankSerializer, ProductSerializer
from .permissions import IsAdminOrReadOnly
from django.db import IntegrityError, transaction
from rest_framework import status
from rest_framework.response import Response
import logging
# --- New ViewSets for Bank and Product Management ---
logger = logging.getLogger(__name__)

class BankViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing Banks (Admin CRUD, Others Read-Only).
    Includes detailed error logging.
    """
    queryset = Bank.objects.all()
    serializer_class = BankSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]

    def list(self, request, *args, **kwargs):
        try:
            return super().list(request, *args, **kwargs)
        except Exception as e:
            logger.error(f"[BankViewSet] Error in LIST: {str(e)}", exc_info=True)
            return Response({"detail": "Internal server error"}, status=500)

    def retrieve(self, request, *args, **kwargs):
        try:
            return super().retrieve(request, *args, **kwargs)
        except Exception as e:
            logger.error(f"[BankViewSet] Error in RETRIEVE: {str(e)}", exc_info=True)
            return Response({"detail": "Internal server error"}, status=500)

    def create(self, request, *args, **kwargs):
        try:
            logger.info(f"[BankViewSet] CREATE request data: {request.data}")
            return super().create(request, *args, **kwargs)
        except Exception as e:
            logger.error(f"[BankViewSet] Error in CREATE: {str(e)}", exc_info=True)
            return Response({"detail": "Internal server error"}, status=500)

    def update(self, request, *args, **kwargs):
        try:
            logger.info(f"[BankViewSet] UPDATE request data: {request.data}")
            return super().update(request, *args, **kwargs)
        except Exception as e:
            logger.error(f"[BankViewSet] Error in UPDATE: {str(e)}", exc_info=True)
            return Response({"detail": "Internal server error"}, status=500)

    def destroy(self, request, *args, **kwargs):
        try:
            logger.warning(f"[BankViewSet] DELETE attempt for ID: {kwargs.get('pk')}")
            return super().destroy(request, *args, **kwargs)
        except Exception as e:
            logger.error(f"[BankViewSet] Error in DELETE: {str(e)}", exc_info=True)
            return Response({"detail": "Internal server error"}, status=500)

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
    # We remove the static 'queryset' attribute and use get_queryset instead
    serializer_class = LinkSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]

    def get_queryset(self):
        """
        Custom queryset to filter Links based on the user's role.
        """
        user = self.request.user
        
        # Base queryset with select_related optimization 
        # (fetches bank/product data in 1 query to speed up the Serializer)
        qs = Link.objects.select_related('bank', 'product').order_by('bank__name', 'product__name')

        # Safety check
        if not user.is_authenticated:
            return Link.objects.none()

        # 1. ADMIN: Sees ALL links
        if user.role == 'ADMIN':
            return qs
        
        # 2. STAFF / CONNECTOR: Sees only links associated with their assigned products
        # This looks at the User.products ManyToMany field
        return qs.filter(product__in=user.products.all())

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