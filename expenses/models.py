from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    """ Extend the default User model to include roles and manager relationship. """
    ROLE_CHOICES = (
        ('employee', 'Employee'),
        ('manager', 'Manager'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='employee')
    manager = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='team_members'
    )

    def __str__(self):
        return f"{self.user.username} - {self.get_role_display()}"


class Expense(models.Model):
    """ Represents a single expense entry by an employee. """
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )
    CATEGORY_CHOICES = (
        ('travel', 'Travel'),
        ('food', 'Food'),
        ('software', 'Software'),
        ('other', 'Other'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='expenses')
    date = models.DateField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    receipt = models.ImageField(upload_to='receipts/', null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.category} - ${self.amount}"


class Report(models.Model):
    """ Represents a collection of expenses submitted for approval. """
    STATUS_CHOICES = (
        ('submitted', 'Submitted'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reports')
    manager = models.ForeignKey(User, on_delete=models.PROTECT, related_name='reports_to_approve')
    name = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    comments = models.TextField(blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='submitted')
    expenses = models.ManyToManyField(Expense, related_name='reports')
    submitted_at = models.DateTimeField(auto_now_add=True)

    @property
    def total_amount(self):
        return self.expenses.aggregate(total=models.Sum('amount'))['total'] or 0.00

    def __str__(self):
        return f"Report: {self.name} by {self.user.username}"

