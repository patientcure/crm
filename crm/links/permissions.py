# links/permissions.py
from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow ADMINs to create, update, or delete.
    Allows Staff and Connector (safe methods) read access.
    """
    def has_permission(self, request, view):
        # Read permissions are allowed to any authenticated request (Admin, Staff, Connector)
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
        
        # Write permissions are only allowed to ADMINs
        return request.user and request.user.is_authenticated and request.user.role == 'ADMIN'