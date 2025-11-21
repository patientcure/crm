from django.contrib.auth.models import AbstractUser
from django.db import models
from links.models import Product

class User(AbstractUser):
    ROLE_CHOICES = (
        ('ADMIN', 'Admin'),
        ('STAFF', 'Staff'),
        ('CONNECTOR', 'Connector'),
    )
    
    phone = models.CharField(max_length=15, unique=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='CONNECTOR')
    products = models.ManyToManyField(Product, blank=True, help_text="Products assigned to the user (for Staff/Connector).")

    created_at = models.DateTimeField(auto_now_add=True, null=True)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['username','email', 'first_name']
    
    def __str__(self):
        return f"{self.phone} ({self.role})"

    # --- ADD THESE PROPERTIES BELOW ---
    @property
    def is_admin(self):
        return self.role == 'ADMIN'

    @property
    def is_staff_member(self):
        # Renamed to avoid conflict with Django's built-in is_staff
        return self.role == 'STAFF'

    @property
    def is_connector(self):
        return self.role == 'CONNECTOR'
    
    
class TermsAndConditions(models.Model):
    """
    Model to store Terms and Conditions content.
    """
    content = models.TextField(help_text="Terms and Conditions content in HTML format.")
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        help_text="The admin user who last updated the Terms and Conditions."
    )
    def __str__(self):
        return f"Terms and Conditions (Last updated: {self.updated_at.strftime('%Y-%m-%d %H:%M:%S')})"