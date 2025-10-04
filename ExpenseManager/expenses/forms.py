from django import forms
from .models import Expense, Receipt

# Define a shared style dictionary to match your dark/light contrast needs
INPUT_STYLE = {
    # Sets the text color to dark for contrast against the light input box (c5eaea)
    'class': 'w-full px-4 py-2 border rounded-lg text-dark bg-light-input border-slate-700 placeholder-slate-500' 
}
TEXTAREA_STYLE = INPUT_STYLE.copy()
TEXTAREA_STYLE.update({'rows': 3})

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['category', 'amount', 'currency', 'description', 'date']
        widgets = {
            # Apply styling to input fields
            'amount': forms.NumberInput(attrs=INPUT_STYLE),
            'currency': forms.TextInput(attrs=INPUT_STYLE),
            'description': forms.Textarea(attrs=TEXTAREA_STYLE),
            # Set the date input type and apply styling
            'date': forms.DateInput(attrs={'type': 'date', **INPUT_STYLE}),
            'category': forms.Select(attrs=INPUT_STYLE),
        }

class ReceiptForm(forms.ModelForm):
    class Meta:
        model = Receipt
        fields = ['image']
