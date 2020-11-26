from django.shortcuts import render
from django.http import HttpResponse
from shop.views import login_view, registration_view
from shop.models import Store
from .forms import StoreRegistrationForm


def home(req):
    context = {'title': 'home', 'user': 'store', 'user_name': req.session.get('user_name')}
    return render(req, 'store/home.html', context)


def store_login_view(req):
    """Class to handle Store login view."""
    return login_view(req, user='store', database=Store, ret='home.store')


def store_registration_view(req):
    """Function to handle Store registration view."""
    return registration_view(req, user='store', ret='login.store', reg_form=StoreRegistrationForm)
