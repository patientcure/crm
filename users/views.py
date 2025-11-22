# users/views.py
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import User, TermsAndConditions, HomePage
from .serializers import (
    UserRegistrationSerializer, 
    UserSerializer, 
    UserDetailSerializer,
    TermsAndConditionsSerializer,
    HomePageSerializer
)
from .permissions import IsAdminUser
from customers.models import Customer
from links.models import Product
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import uuid
import json

class UserRegistrationAPIView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        return Response({
            "message": f"User {user.phone} ({user.role}) created successfully",
            "user": {
                "id": user.id,
                "phone": user.phone,
                "first_name": user.first_name,
                "role": user.role,
                "created_at": user.created_at
            }
        }, status=status.HTTP_201_CREATED)

class UserProfileAPIView(generics.RetrieveAPIView):
    """
    Get current user profile (Self)
    Uses standard serializer (no customer list needed usually for self profile unless requested)
    """
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        return self.request.user

class UserListAPIView(generics.ListAPIView):
    queryset = User.objects.all().prefetch_related('products')  # add prefetch
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]


class UserDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    Admin View: Retrieve single user with FULL details (including referred customers).
    """
    # Use the serializer that includes 'referred_customers'
    serializer_class = UserDetailSerializer 
    permission_classes = [IsAuthenticated, IsAdminUser]
    lookup_field = "pk"

    def get_queryset(self):
        """
        Optimize query to fetch customers, banks, and products efficiently.
        """
        return User.objects.prefetch_related(
            'products',
            'customer_set', 
            'customer_set__referred_for_product',
            'customer_set__referred_for_product__bank',
            'customer_set__referred_for_product__product'
        )

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", True)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(
            {"message": f"User {instance.phone} updated successfully.", "user": serializer.data},
            status=status.HTTP_200_OK,
        )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        phone = getattr(instance, "phone", str(instance.pk))
        self.perform_destroy(instance)
        return Response({"message": f"User {phone} deleted successfully."}, status=status.HTTP_200_OK)
    
class TermsAndConditionsAPIView(generics.RetrieveUpdateAPIView):
    queryset = TermsAndConditions.objects.all()
    serializer_class = TermsAndConditionsSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH']:
            self.permission_classes.append(IsAdminUser)
        return super().get_permissions()

    def get_object(self):
        return self.queryset.first()

class HomePageAPIView(generics.RetrieveUpdateAPIView):
    queryset = HomePage.objects.all()
    serializer_class = HomePageSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH']:
            self.permission_classes = [IsAuthenticated, IsAdminUser]
        return super().get_permissions()

    def get_object(self):
        obj = self.queryset.first()
        if not obj:
            obj = HomePage.objects.create()
        return obj

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        live_stats = {
            "total_customers": Customer.objects.count(),
            "total_staff": User.objects.filter(role='STAFF').count(),
            "total_connectors": User.objects.filter(role='CONNECTOR').count(),
            "total_admins": User.objects.filter(role='ADMIN').count(),
            "total_products": Product.objects.count(),
        }
        data = serializer.data
        data['live_stats'] = live_stats
        return Response(data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        """
        Accept multipart/form-data for image uploads:
        - files should be sent as 'images' (multiple)
        - optional metadata JSON (string) can be sent as 'slider_images' containing list of dicts.
        """
        instance = self.get_object()

        # Parse slider_images metadata if provided (could be JSON string)
        slider_meta = None
        raw_meta = request.data.get('slider_images')
        if raw_meta:
            try:
                slider_meta = json.loads(raw_meta) if isinstance(raw_meta, str) else raw_meta
            except Exception:
                slider_meta = None

        # Handle uploaded files
        uploaded_files = request.FILES.getlist('images')
        saved_entries = []

        for f in uploaded_files:
            # save file with unique name under homepage_sliders/
            filename = f"{uuid.uuid4().hex}_{f.name}"
            path = default_storage.save(f"homepage_sliders/{filename}", ContentFile(f.read()))

            # get storage URL (respects MEDIA_URL and storage backend)
            try:
                storage_url = default_storage.url(path)
            except Exception:
                media_url = getattr(settings, 'MEDIA_URL', '/media/')
                if not media_url.endswith('/'):
                    media_url = media_url + '/'
                storage_url = media_url + path.lstrip('/')

            # build absolute URL
            img_url = request.build_absolute_uri(storage_url)

            # find matching metadata by original filename if provided
            meta = {}
            if slider_meta:
                for m in list(slider_meta):
                    if m.get('filename') and m.get('filename') == f.name:
                        meta = m
                        slider_meta.remove(m)
                        break

            entry = {
                'image': img_url,
                'caption': meta.get('caption', ''),
                'order': meta.get('order', 0),
                'is_active': meta.get('is_active', True)
            }
            saved_entries.append(entry)

        # If metadata (without files) provided -> use it to replace slider_images
        if slider_meta is not None and not uploaded_files:
            # expect metadata entries to already contain 'image' (URL/path)
            new_list = slider_meta
        else:
            # merge existing stored entries (unless metadata commanded full replace)
            # If metadata provided alongside uploaded files, append saved_entries and remaining metadata (if any)
            new_list = []
            # If client wants full replace, they can send 'replace' flag in request.data
            replace_flag = request.data.get('replace', 'false').lower() == 'true'
            if not replace_flag:
                # start with current entries
                new_list.extend(instance.slider_images or [])
            # append saved entries (new uploads)
            new_list.extend(saved_entries)
            # append leftover metadata entries (if any) assuming they already have 'image' url/path
            if slider_meta:
                for m in slider_meta:
                    # ensure required keys
                    entry = {
                        'image': m.get('image'),
                        'caption': m.get('caption', ''),
                        'order': m.get('order', 0),
                        'is_active': m.get('is_active', True)
                    }
                    new_list.append(entry)

        # Prepare payload for serializer (replace slider_images)
        payload = request.data.copy()
        # ensure payload uses JSON-serializable Python structures
        payload['slider_images'] = new_list

        serializer = self.get_serializer(instance, data=payload, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({"message": "Homepage updated.", "homepage": serializer.data}, status=status.HTTP_200_OK)