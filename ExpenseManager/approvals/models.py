from django.db import models
from django.conf import settings
from expenses.models import Expense

class Approval(models.Model):
    class Decision(models.TextChoices):
        APPROVED = 'APPROVED', 'Approved'
        REJECTED = 'REJECTED', 'Rejected'

    expense = models.ForeignKey(Expense, on_delete=models.CASCADE, related_name='approvals')
    manager = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    decision = models.CharField(max_length=10, choices=Decision.choices)
    comments = models.TextField(blank=True)
    reviewed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['expense', 'manager'], name='unique_manager_review')
        ]

    def __str__(self):
        return f"Review of {self.expense} by {self.manager.username} - {self.get_decision_display()}"