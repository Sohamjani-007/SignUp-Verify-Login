# accounts/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django.contrib.auth.forms import AuthenticationForm


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    mobile = forms.CharField(required=True)

    class Meta:
        model = CustomUser
        fields = (
            "username",
            "first_name",
            "last_name",
            "mobile",
            "email",
            "password1",
            "password2",
        )


class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=30, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
