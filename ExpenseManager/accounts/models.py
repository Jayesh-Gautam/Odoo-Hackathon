from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import Q


class Company(models.Model):
    name = models.CharField(max_length=100, unique=True)
    default_currency = models.CharField(max_length=3, default='USD')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class CustomUser(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = 'ADMIN', 'Admin'
        MANAGER = 'MANAGER', 'Manager'
        EMPLOYEE = 'EMPLOYEE', 'Employee'

    base_role = Role.ADMIN

    role = models.CharField(max_length=50, choices=Role.choices, default=base_role)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)
    managers = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='subordinates',
        blank=True
    )

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        # Store original state if the instance is being updated
        if self.pk:
            try:
                old_instance = CustomUser.objects.get(pk=self.pk)
                # Check if the role is being changed from a managing role to a non-managing one
                was_manager = old_instance.role in [self.Role.ADMIN, self.Role.MANAGER]
                is_now_employee = self.role == self.Role.EMPLOYEE

                if was_manager and is_now_employee:
                    # If the user is demoted, they can no longer be a manager for anyone.
                    # This clears the relationship from their former subordinates.
                    self.subordinates.clear()
            except CustomUser.DoesNotExist:
                # This can happen in rare cases like fixture loading.
                pass

        super().save(*args, **kwargs)

    class Meta:
        # Enforce that a company can only have one user with the 'ADMIN' role.
        constraints = [
            models.UniqueConstraint(
                fields=['company'],
                condition=Q(role='ADMIN'),
                name='one_admin_per_company'
            )
        ]

