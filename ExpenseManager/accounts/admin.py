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


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Company)

