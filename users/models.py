# users/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('ADMIN', 'Admin'),
        ('STAFF', 'Staff'),
        ('CONNECTOR', 'Connector'),
    )
    
    phone = models.CharField(max_length=15, unique=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='CONNECTOR')
    
    # Use phone as the username field instead of username
    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['email', 'first_name']
    
    def __str__(self):
        return f"{self.phone} ({self.role})"