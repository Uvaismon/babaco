from django.shortcuts import render
from shop.views import registration_view, login_view
from .forms import CustomerRegistrationForm
from shop.models import Customer
from shop.forms import LoginForm


def home(req):
    context = {'title': 'home', 'user': 'user', 'user_name': req.session.get('user_name')}
    return render(req, 'user/home.html', context)


def customer_registration_view(req):
    """Function to handle customer registration view."""
    return registration_view(req, user='user', reg_form=CustomerRegistrationForm, ret='login')


def customer_login_view(req):
    """Class to handle Customer login view."""
    return login_view(req, user='user', database=Customer, ret='home')
