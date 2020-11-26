from shop.forms import RegistrationForm
from django.forms import ModelForm, PasswordInput, CharField, Textarea, TextInput, NumberInput
from shop.models import Customer


class CustomerRegistrationForm(RegistrationForm):
    """Form to handle Customer registration."""

    class Meta:
        model = Customer
        fields = ['name', 'email', 'password']
        widgets = {
            'password': PasswordInput(),
        }