from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm as BaseUserChangeForm
from .models import CustomUser, Company

class CustomUserCreationForm(UserCreationForm):
    """
    A form for creating new users. Includes a field for company name
    to create a new company during signup.
    """
    company_name = forms.CharField(max_length=100, help_text='The name of your company.')

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('email',)

class ProfileUpdateForm(forms.ModelForm):
    """
    A form for updating user profiles. It dynamically adjusts the 'managers'
    field based on the user's role and permissions.
    """
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'managers']

    def __init__(self, *args, **kwargs):
        self.request_user = kwargs.pop('request_user', None)
        super(ProfileUpdateForm, self).__init__(*args, **kwargs)

        user_company = self.instance.company

        if self.request_user and user_company and \
           (self.request_user.role in [CustomUser.Role.ADMIN, CustomUser.Role.MANAGER]):

            self.fields['managers'].queryset = CustomUser.objects.filter(
                company=user_company,
                role__in=[CustomUser.Role.ADMIN, CustomUser.Role.MANAGER]
            ).exclude(pk=self.instance.pk)
            self.fields['managers'].help_text = 'Select one or more managers.'
        else:
            del self.fields['managers']

class CustomUserChangeForm(BaseUserChangeForm):
    """A form for updating users in the admin, with filtered manager choices."""
    class Meta(BaseUserChangeForm.Meta):
        model = CustomUser
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user_instance = self.instance

        # Ensure the 'managers' field exists and the user belongs to a company
        if 'managers' in self.fields and user_instance and user_instance.company:
            # Only Admins and Managers from the same company can be managers
            self.fields['managers'].queryset = CustomUser.objects.filter(
                company=user_instance.company,
                role__in=[CustomUser.Role.ADMIN, CustomUser.Role.MANAGER]
            ).exclude(pk=user_instance.pk)

