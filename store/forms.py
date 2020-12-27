from shop.forms import RegistrationForm
from shop.models import Store, Product
from django.forms import ModelForm, PasswordInput, CharField, Textarea, TextInput, NumberInput, ImageField, HiddenInput


class StoreRegistrationForm(RegistrationForm):
    """Form to handle Store registration"""

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


class AddproductForm(ModelForm):
    """Form to Add new product"""
    class Meta:
        model = Product

        fields = ['name', 'details', 'price', 'category', 'image', 'store_id', 'deliverable']
        widgets = {
            'price': NumberInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update(size='20')
        self.fields['details'].widget.attrs.update(size='10')
        self.fields['price'].widget.attrs.update(size='10')
