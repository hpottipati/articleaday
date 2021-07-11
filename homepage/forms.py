from django import forms

class ProfessionForm(forms.Form):
    profession = forms.CharField(label="Name", required=True, max_length=100)
