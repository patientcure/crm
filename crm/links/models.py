# links/models.py (UPDATED)
from django.db import models
from django.urls import reverse
from users.models import User

class Bank(models.Model):
    """Represents a financial institution."""
    name = models.CharField(max_length=100, unique=True)
    logo = models.ImageField(upload_to='bank_logos/', blank=True, null=True)

    class Meta:
        ordering = ['name']
        
    def __str__(self):
        return self.name

class Product(models.Model):
    """Represents a type of product (e.g., Loan, Account Open, Credit Card)."""
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ['name']
        
    def __str__(self):
        return self.name


class Link(models.Model):
    """
    Table of links for specific Bank and Product combinations.
    """
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    
    # Renamed from 'name' to combine bank/product info easily in UI
    name = models.CharField(max_length=150, help_text="Specific campaign name (e.g., 'HDFC Personal Loan 2024 Offer')") 
    
    # The base URL that customers are eventually redirected to
    utm_link = models.URLField(help_text="The final destination/UTM link for the bank")
    
    # Optional fields for credentials
    user_id = models.CharField(max_length=100, blank=True, null=True, help_text="Optional bank portal User ID")
    password = models.CharField(max_length=100, blank=True, null=True, help_text="Optional bank portal Password")
    
    image = models.ImageField(upload_to='link_images/', blank=True, null=True, help_text="Product image/logo")

    # This is a fixed internal link for customer onboarding (used for tracking)
    internal_customer_onboarding_url = models.CharField(
        max_length=255, 
        editable=False, 
        help_text="Internal URL pattern: /onboard/<link_id>/<user_id>/"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['bank', 'product'], name='unique_bank_product')
        ] 

    def save(self, *args, **kwargs):
        is_new = self._state.adding
        super().save(*args, **kwargs)
        if is_new or not self.internal_customer_onboarding_url:
            self.internal_customer_onboarding_url = reverse('customer_onboarding_base', kwargs={'link_id': self.id})
            # To avoid recursion, we re-save only if the internal URL changes
            Link.objects.filter(id=self.id).update(internal_customer_onboarding_url=self.internal_customer_onboarding_url)

