from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from account.models import Account

from django import forms
from .models import Account

class RegisterForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ["username", "email", "password"]


class AccountAuthenticationForm(forms.ModelForm):

    class Meta:
        model = Account
        fields = ['email', 'password']

    def clean(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']
            if not authenticate(email, password):
                raise forms.ValidationError("Invalid login")