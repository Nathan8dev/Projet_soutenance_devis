from django import forms
from .models import Client

class Inscription(forms.ModelForm):
    class Meta:
        model = Client
        fields = '__all__'