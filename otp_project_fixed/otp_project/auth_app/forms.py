from django import forms
from .models import UserOTP

class RegisterForm(forms.ModelForm):
    class Meta:
        model = UserOTP
        fields = ['name', 'phone']
