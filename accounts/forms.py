from django import forms
from django.contrib.auth.models import User
from .models import Profile
from django.contrib.auth.forms import AuthenticationForm


class AuthenticationFormWithChekUsersStatus(AuthenticationForm):
    def confirm_login_allowed(self, user):
        if not user.status == 'enabled':
            raise forms.ValidationError(
                "Your account has disabled.",
                code='inactive',
            )


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']
