from django import forms
from .models import Expense, Receipt

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['category', 'amount', 'currency', 'description', 'date']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'})
        }

class ReceiptForm(forms.ModelForm):
    class Meta:
        model = Receipt
        fields = ['image']