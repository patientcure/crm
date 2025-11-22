# users/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User,HomePageSlider, TermsAndConditions  

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    # Add phone and role to list display
    list_display = ('phone', 'username', 'email', 'first_name', 'last_name', 'role', 'is_staff')
    list_filter = ('role', 'is_staff', 'is_superuser', 'is_active')
    search_fields = ('phone', 'username', 'first_name', 'last_name', 'email')
    
    # Update fieldsets to include new fields
    fieldsets = (
        (None, {'fields': ('phone', 'username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'role')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions','products')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    # Update add fieldsets
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone', 'username', 'email', 'first_name', 'last_name', 'role', 'password1', 'password2'),
        }),
    )
    
    # Order by phone by default
    ordering = ('phone',)

@admin.register(HomePageSlider)
class HomePageSliderAdmin(admin.ModelAdmin):
    list_display = ('id', 'caption', 'order', 'is_active', 'created_at', 'updated_at')
    list_filter = ('is_active',)
    search_fields = ('caption',)
    ordering = ('order',)   
@admin.register(TermsAndConditions)
class TermsAndConditionsAdmin(admin.ModelAdmin):
    list_display = ('id', 'updated_at', 'updated_by')
    search_fields = ('content', 'updated_by__phone', 'updated_by__first_name', 'updated_by__last_name')
    ordering = ('-updated_at',)