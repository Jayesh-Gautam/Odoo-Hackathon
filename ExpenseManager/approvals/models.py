from django.db import models
from django.conf import settings
from expenses.models import Company, Expense

class ApprovalFlow(models.Model):
    """
    Defines a sequence of approvers for a company.
    An expense will be linked to one of these flows.
    """
    name = models.CharField(max_length=255)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='approval_flows')
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} for {self.company.name}"

class ApprovalStep(models.Model):
    """
    Represents a single step in an ApprovalFlow, defining the approver.
    """
    approval_flow = models.ForeignKey(ApprovalFlow, on_delete=models.CASCADE, related_name='steps')
    approver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    sequence = models.PositiveIntegerField(help_text="Order of approval (e.g., 1, 2, 3...).")

    class Meta:
        ordering = ['sequence']

    def __str__(self):
        return f"Step {self.sequence}: {self.approver.username} in {self.approval_flow.name}"

class ApprovalRule(models.Model):
    """
    Defines conditional approval logic for a flow.
    """
    RULE_TYPE_CHOICES = (
        ('percentage', 'Percentage'),
        ('specific', 'Specific Approver'),
        ('hybrid', 'Hybrid'),
    )
    approval_flow = models.OneToOneField(ApprovalFlow, on_delete=models.CASCADE, related_name='rule')
    rule_type = models.CharField(max_length=20, choices=RULE_TYPE_CHOICES)
    
    # For 'percentage' rule
    percentage_required = models.PositiveIntegerField(null=True, blank=True, help_text="e.g., 60 for 60%")
    
    # For 'specific' rule
    specific_approver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Rule for {self.approval_flow.name}"

class ApprovalLog(models.Model):
    """
    Stores a log of all actions taken on an expense approval.
    """
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )
    expense = models.ForeignKey(Expense, on_delete=models.CASCADE, related_name='approval_logs')
    approver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    comment = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    step = models.ForeignKey(ApprovalStep, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ['timestamp']
    
    def __str__(self):
        return f"{self.get_status_display()} by {self.approver.username} for {self.expense.title}"
