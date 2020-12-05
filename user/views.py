from django.shortcuts import render, redirect

from babaco import settings
from shop.views import registration_view, login_view
from .forms import CustomerRegistrationForm
from shop.models import Customer, Product
from shop.forms import LoginForm


def home(req):
    products = Product.objects.all()[:12]    # dbtrans
    context = {'title': 'home', 'user': 'user', 'user_name': req.session.get('user_name'),
               'products': products, 'media_url': settings.MEDIA_URL}
    return render(req, 'user/home.html', context)


def customer_registration_view(req):
    """Function to handle customer registration view."""
    return registration_view(req, user='user', reg_form=CustomerRegistrationForm, ret='login')


def customer_login_view(req):
    """Class to handle Customer login view."""
    return login_view(req, user='user', database=Customer, ret='home')


def userprofile(req):
    if req.session.get('user_id'):
        customer_id = Customer.objects.get(pk=req.session.get('user_id'))      # dbtrans
        context = {'customer_id': customer_id, 'title': 'profile'}
        return render(req, 'user/userprofile.html',context)
    else:
        return redirect('login/')

def logout(req):
    req.session.flush()
    return redirect('home')
