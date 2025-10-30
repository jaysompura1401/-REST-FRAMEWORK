from django import forms
from .models import Doctor
class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['name','specialty','address','city']
        widgets = {
            'address': forms.TextInput(attrs={'placeholder': 'Street address, area...'}),
            'city': forms.TextInput(attrs={'placeholder': 'City name'}),
        }
