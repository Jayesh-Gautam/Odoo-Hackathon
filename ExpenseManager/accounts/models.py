from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class Company(models.Model):
    """
    Stores information about a company.
    """
    name = models.CharField(max_length=255, help_text="The legal name of the company.")
    address = models.TextField(blank=True, null=True, help_text="The physical address of the company.")
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    # In a real-world scenario, you might fetch currency choices from an API.
    # For simplicity, we'll use a CharField here.
    default_currency = models.CharField(max_length=3, default='USD', help_text="Default 3-letter currency code (e.g., USD, EUR).")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Company"
        verbose_name_plural = "Companies"
        ordering = ['name']


class CustomUser(AbstractUser):
    """
    Extends the default Django User model.
    """
    class Role(models.TextChoices):
        """
        Enum-like choices for user roles.
        """
        ADMIN = 'ADMIN', _('Admin')
        MANAGER = 'MANAGER', _('Manager')
        EMPLOYEE = 'EMPLOYEE', _('Employee')

    # Add your custom fields here
    role = models.CharField(
        _('role'),
        max_length=50,
        choices=Role.choices,
        default=Role.EMPLOYEE,
        help_text="The role of the user within the company."
    )
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='users',
        help_text="The company this user belongs to."
    )
    manager = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='subordinates',
        help_text="The user's direct manager."
    )

    # We need to specify a custom related_name for groups and user_permissions
    # to avoid clashes with the default User model.
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name=_('groups'),
        blank=True,
        help_text=_(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
        related_name="customuser_set",
        related_query_name="user",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name=_('user permissions'),
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_name="customuser_set",
        related_query_name="user",
    )

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        # Ensure that a user cannot be their own manager
        if self.manager == self:
            raise ValueError("A user cannot be their own manager.")
        super().save(*args, **kwargs)
