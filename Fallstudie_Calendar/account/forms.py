# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from account.models import Account

# Form for user registration, inheriting from UserCreationForm
class RegistrationForm(UserCreationForm):
    class Meta:
        model = Account  # Specifies the model to be used
        fields = ("email", "username", "password1", "password2")  # Fields to be included in the form

# Form for authenticating users
class AccountAuthenticationForm(forms.ModelForm):
    class Meta:
        model = Account  # Specifies the model to be used
        fields = ('email', 'password')  # Fields to be included in the form

    # Method to clean and validate the form data
    def clean(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']
            if not authenticate(email=email, password=password):  # Check if the user exists
                raise forms.ValidationError('E-Mail oder Passwort sind falsch.')

# Form for updating user account details
class AccountUpdateForm(forms.ModelForm):
    class Meta:
        model = Account  # Specifies the model to be used
        exclude = ()  # Excludes no fields, includes all fields by default
