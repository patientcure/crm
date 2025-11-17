# customers/permissions.py
from rest_framework import permissions

class IsAdminOrOwnCustomer(permissions.BasePermission):
    """
    Admin can see and edit all. 
    Staff/Connector can only see customers they referred.
    """
    def has_permission(self, request, view):
        # Allow all authenticated users read permission (handled in queryset filtering)
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
        
        # Only Admin can use POST/PUT/DELETE
        return request.user and request.user.is_authenticated and request.user.role == 'ADMIN'