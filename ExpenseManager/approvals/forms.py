from django import forms
from .models import Approval

class ReviewForm(forms.Form):
    decision = forms.ChoiceField(choices=Approval.Decision.choices, widget=forms.RadioSelect)
    comments = forms.CharField(widget=forms.Textarea, required=False)