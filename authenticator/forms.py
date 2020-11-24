from django.forms import ModelForm, PasswordInput, CharField, Textarea, TextInput, NumberInput
from store.models import Customer, Store
import re
import logging

logging.basicConfig(level='DEBUG', filename='debug.log')


class RegistrationForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update(size='30')
        self.fields['email'].widget.attrs.update(size='30')
        self.fields['password'].widget.attrs.update(size='30')
        self.fields['password1'].widget.attrs.update(size='30')

    password1 = CharField(widget=PasswordInput(), label='Confirm password')

    def verify(self):
        self.is_valid()
        if self.cleaned_data['password'] != self.cleaned_data['password1']:
            self.add_error('password', 'Password confirmation failed')
        if re.search(r'[^a-zA-Z .]', self.cleaned_data['name']):
            self.add_error('name', 'Invalid name')


class CustomerRegistrationForm(RegistrationForm):
    class Meta:
        model = Customer
        fields = ['name', 'email', 'password']
        widgets = {
            'password': PasswordInput(),
        }


class StoreRegistrationForm(RegistrationForm):
    class Meta:
        model = Store
        fields = ['name', 'email', 'contact', 'location', 'password']
        widgets = {
            'password': PasswordInput(),
            'location': TextInput(),
            'contact': NumberInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['location'].widget.attrs.update(size='30')
        self.fields['contact'].widget.attrs.update(size='30')
