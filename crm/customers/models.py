# customers/models.py
from django.db import models
from links.models import Link
from users.models import User
class Customer(models.Model):
    """
    Model to store customer details and tracking information.
    """
    # Customer Details
    name = models.CharField(max_length=150)
    phone = models.CharField(max_length=15)
    email = models.EmailField(blank=True, null=True)
    pan = models.CharField(max_length=10, help_text="Customer PAN number (Unique identifier)", unique=True)
    
    # Tracking/Referral
    referred_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        limit_choices_to={'role__in': ['STAFF', 'CONNECTOR']}, 
        help_text="The Staff/Connector who shared the unique link."
    )
    referred_for_product = models.ForeignKey(
        Link,
        on_delete=models.SET_NULL,
        null=True,
        help_text="The bank product the customer was referred for."
    )
    
    # Commission Field (Manually edited by Admin)
    commission_amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0.00, 
        help_text="Admin can manually add commission for the referring Staff/Connector."
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # Constraint to ensure unique PAN
        pass 

    def __str__(self):
        return self.name
