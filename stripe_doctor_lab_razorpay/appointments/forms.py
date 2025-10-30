from django import forms
class BookingForm(forms.Form):
    name = forms.CharField(max_length=100)
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
