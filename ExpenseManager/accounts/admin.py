from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Company

class CustomUserAdmin(UserAdmin):
    """
    Configuration for the CustomUser model in the Django admin site.
    """
    model = CustomUser
    # Add custom fields to the list display
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'company', 'is_staff')
    # Add custom fields to the fieldsets for the add/change forms
    fieldsets = UserAdmin.fieldsets + (
        ('Company Info', {'fields': ('company', 'role', 'manager')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Company Info', {'fields': ('company', 'role', 'manager')}),
    )
    # Add filtering capabilities
    list_filter = ('role', 'company', 'is_staff', 'is_superuser', 'groups')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('username',)

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    """
    Configuration for the Company model in the Django admin site.
    """
    list_display = ('name', 'phone_number', 'default_currency', 'created_at')
    search_fields = ('name', 'default_currency')
    ordering = ('name',)

# Register the CustomUser model with the custom admin class
admin.site.register(CustomUser, CustomUserAdmin)
