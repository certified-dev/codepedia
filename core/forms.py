from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={'placeholder': 'Enter email address'}), required=True)

    class Meta(UserCreationForm.Meta):
        model = User
