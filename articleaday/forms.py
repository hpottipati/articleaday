from dataclasses import field
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class ProfessionForm(forms.Form):
    profession = forms.CharField(label="Name", required=True, max_length=100)

