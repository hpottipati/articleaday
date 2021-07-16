from dataclasses import field
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from matplotlib.pyplot import cla


class ProfessionForm(forms.Form):
    profession = forms.CharField(label="Name", required=True, max_length=100)
    check = forms.BooleanField(required=True)


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class LoginForm(UserCreationForm):
    class Meta:
        fields = ['username', 'password']
