from django.shortcuts import render, redirect
from django.http import HttpResponse
from shop.views import login_view, registration_view
from shop.models import Store, Product
from .forms import StoreRegistrationForm, AddproductForm
from babaco.settings import MEDIA_URL
from django.contrib import messages
from shop.tests import logging


def home(req):
    if not req.session.get('store_id'):
        return redirect(store_login_view)
    store = Store.objects.get(pk=req.session.get('store_id'))    # db trans
    products = Product.objects.filter(store_id=store)   # db trans
    context = {'title': 'home', 'user': 'store', 'store_name': req.session.get('store_name'),
               'products': products, 'media_url': MEDIA_URL}
    return render(req, 'store/home.html', context)


def store_login_view(req):
    """Class to handle Store login view."""
    return login_view(req, user='store', database=Store, ret='home.store')


def store_registration_view(req):
    """Function to handle Store registration view."""
    return registration_view(req, user='store', ret='login.store', reg_form=StoreRegistrationForm)


def store_addproduct_view(req):
    if not req.session.get('store_id'):
        return redirect(store_login_view)
    store_id = req.session.get('store_id')
    # Checking if its a POST request and handle it.
    if req.method == 'POST':
        post = req.POST.copy()
        post['store_id'] = Store.objects.get(pk=store_id)                                                      # dbtrans
        form = AddproductForm(post, req.FILES)
        if form.is_valid():
            form.save()
            return redirect(home)
    else:
        form = AddproductForm()
    context = {'form': form, 'title': 'add product', 'store_name': req.session.get('store_name')}
    return render(req, 'store/addproduct.html', context)


def profile(req):
    if req.session.get('store_id'):
        store_id = Store.objects.get(pk=req.session.get('store_id'))  # dbtrans
        context = {'store_id': store_id, 'title': 'profile', 'user': 'store',
                   'store_name': req.session.get('store_name')}
        return render(req, 'store/profile.html', context)
    else:
        return redirect('store/login/')


def logout(req):
    req.session.flush()
    return redirect('home')
