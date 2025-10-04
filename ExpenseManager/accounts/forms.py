from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm as BaseUserChangeForm
from .models import CustomUser, Company

# Define common styling for form inputs
text_input_styles = {
    'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'
}

class CustomUserCreationForm(UserCreationForm):
    company_name = forms.CharField(max_length=100, help_text='The name of your company.', widget=forms.TextInput(attrs=text_input_styles))

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('email',)
        widgets = {
            'username': forms.TextInput(attrs=text_input_styles),
            'email': forms.EmailInput(attrs=text_input_styles),
        }

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['password2'].widget.attrs.update(text_input_styles)
        self.fields['password1'].widget.attrs.update(text_input_styles)


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'managers']
        widgets = {
            'first_name': forms.TextInput(attrs=text_input_styles),
            'last_name': forms.TextInput(attrs=text_input_styles),
            'email': forms.EmailInput(attrs=text_input_styles),
            'managers': forms.SelectMultiple(attrs=text_input_styles),
        }

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
    class Meta(BaseUserChangeForm.Meta):
        model = CustomUser
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user_instance = self.instance

        if 'managers' in self.fields and user_instance and user_instance.company:
            self.fields['managers'].queryset = CustomUser.objects.filter(
                company=user_instance.company,
                role__in=[CustomUser.Role.ADMIN, CustomUser.Role.MANAGER]
            ).exclude(pk=user_instance.pk)


class EditRoleForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['role']
        widgets = {
            'role': forms.Select(attrs=text_input_styles),
        }