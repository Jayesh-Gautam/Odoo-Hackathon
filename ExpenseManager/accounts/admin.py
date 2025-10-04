from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Company

from .forms import CustomUserChangeForm


class CustomUserAdmin(UserAdmin):
    # Use our custom form for the admin change view
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('username', 'email', 'company', 'role', 'is_staff')
    list_filter = ('company', 'role', 'is_staff', 'is_superuser', 'is_active', 'groups')

    fieldsets = UserAdmin.fieldsets + (
        ('Company Info', {'fields': ('company', 'role', 'managers')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Company Info', {'fields': ('company', 'role')}),
    )
    filter_horizontal = ('managers',)

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    """
    Configuration for the Company model in the Django admin site.
    """
    list_display = ('name', 'default_currency', 'created_at')
    search_fields = ('name', 'default_currency')
    ordering = ('name',)

# Register the CustomUser model with the custom admin class
admin.site.register(CustomUser, CustomUserAdmin)
