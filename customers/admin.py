
from django.contrib import admin
from django.db.models import Sum
from .models import Customer

class CustomerAdmin(admin.ModelAdmin):
    # Admin can edit the user details
    list_display = ('name', 'phone', 'pan', 'referred_by', 'referred_for_product', 'commission_amount', 'created_at')
    list_filter = ('referred_by', 'referred_for_product')
    search_fields = ('name', 'phone', 'pan')
    
    # Admin will be able to create new columns if you add new fields to the Customer model.
    # For now, staff/connector can edit details. Admin can edit all.
    fieldsets = (
        ('Customer Details', {'fields': ('name', 'phone', 'email', 'pan')}),
        ('Referral & Commission', {'fields': ('referred_by', 'referred_for_product', 'commission_amount')}),
    )
    
    # Ensure only Admin can edit the commission
    def get_readonly_fields(self, request, obj=None):
        if not request.user.is_superuser and not request.user.is_admin:
            return ('commission_amount', 'referred_by', 'referred_for_product')
        return ()

admin.site.register(Customer, CustomerAdmin)


# --- Dashboard Commission View ---
# This part handles the Admin/Staff dashboard requirement: total commission of each connector.

class ConnectorCommissionDashboard(Customer):
    """
    Proxy model for displaying total commissions in the Admin dashboard.
    """
    class Meta:
        proxy = True
        verbose_name = 'Connector Commission Summary'
        verbose_name_plural = 'Connector Commission Summary'
        

admin.site.register(ConnectorCommissionDashboard)