from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
class ProfessionForm(forms.Form):
    profession = forms.CharField(label="Name", required=True, max_length=100)
    check = forms.BooleanField(required=True) 

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
