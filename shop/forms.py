from django.forms import ModelForm, PasswordInput, CharField, Textarea, TextInput, NumberInput
from django import forms
import re
import logging

logging.basicConfig(level='DEBUG', filename='debug.log')


class RegistrationForm(ModelForm):
    """General form for user registration."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # resize input fields.
        self.fields['name'].widget.attrs.update(size='30')
        self.fields['email'].widget.attrs.update(size='30')
        self.fields['password'].widget.attrs.update(size='30')
        self.fields['password1'].widget.attrs.update(size='30')

    password1 = CharField(widget=PasswordInput(), label='Confirm password')

    def verify(self):
        # Verify validity of data entered in the form.
        self.is_valid()
        if self.cleaned_data['password'] != self.cleaned_data['password1']:
            self.add_error('password', 'Password confirmation failed')
        if re.search(r'[^a-zA-Z .]', self.cleaned_data['name']):
            self.add_error('name', 'Invalid name')


class LoginForm(forms.Form):
    """Form to handle login."""
    email = forms.EmailField()
    password = forms.CharField(widget=PasswordInput(), max_length=30)