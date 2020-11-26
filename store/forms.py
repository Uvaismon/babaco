from shop.forms import RegistrationForm
from shop.models import Store
from django.forms import ModelForm, PasswordInput, CharField, Textarea, TextInput, NumberInput


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
