from shop.forms import RegistrationForm
from django.forms import ModelForm, PasswordInput, CharField, Textarea, TextInput, NumberInput
from shop.models import Customer, Order
from django import forms


class CustomerRegistrationForm(RegistrationForm):
    """Form to handle Customer registration."""

    class Meta:
        model = Customer
        fields = ['name', 'email', 'password']
        widgets = {
            'password': PasswordInput(),
        }


class OrderForm(ModelForm):
    """Form to handle user ordering products"""

    class Meta:
        model = Order
        fields = ['cust_id', 'prod_id', 'date', 'address', 'quantity']


