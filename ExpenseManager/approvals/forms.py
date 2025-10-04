from django import forms
from .models import Approval

class ReviewForm(forms.Form):
    decision = forms.ChoiceField(
        choices=Approval.Decision.choices,
        widget=forms.RadioSelect(attrs={'class': 'mr-2'}),
    )
    comments = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
            'rows': 3
        }),
        required=False
    )