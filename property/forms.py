from django.db.models import fields
from property.models import BookingFile
from django import forms
from django.db.models.fields import TextField
from django.forms.fields import CharField
from django.forms.widgets import Textarea
from django.forms import ModelForm

from .models import User


class AddPropertyForm(forms.Form):
    property_name = forms.CharField(max_length=256)
    street = forms.CharField(max_length=256)
    city = forms.CharField(max_length=256)
    availability = forms.CharField(max_length=256)


class CreateUserForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = CharField(min_length=6, max_length=50)


class CreateNoteForm(forms.Form):
    title = forms.CharField(max_length=200)
    content = forms.CharField(max_length=1000)


class CreateBookingForm(forms.Form):
    client_name = forms.CharField(max_length=255, widget=forms.TextInput(
        attrs={'class': 'form-input mb-5', 'placeholder': 'John Doe'}))
    client_contact = forms.CharField(
        max_length=20, widget=forms.TextInput(attrs={'class': 'form-input mb-5'}))
    client_email = forms.EmailField(max_length=255, widget=forms.EmailInput(
        attrs={'class': 'form-input mb-5', 'placeholder': 'johndoe@gmail.com'}))
    deposit = forms.DecimalField(min_value=0, decimal_places=2, max_digits=15, widget=forms.NumberInput(
        attrs={'class': 'form-input mb-5', 'placeholder': 5000}))
    files = forms.FileField(widget=forms.ClearableFileInput(
        attrs={'multiple': True, 'class': 'ml-4'}), required=False)


# Model Form
class EditUserUsernameForm(ModelForm):
    class Meta:
        model = User
        fields = ['username']


class EditUserEmailForm(ModelForm):
    class Meta:
        model = User
        fields = ['email']


class EditUserContactForm(ModelForm):
    class Meta:
        model = User
        fields = ['contact']


class EditUserPasswordForm(ModelForm):
    class Meta:
        model = User
        fields = ['password']
