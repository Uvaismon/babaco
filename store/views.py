from django.shortcuts import render, redirect
from django.http import HttpResponse
from shop.views import login_view, registration_view
from shop.models import Store, Product
from .forms import StoreRegistrationForm, AddproductForm
from django.contrib import messages
from shop.tests import logging


def home(req):
    context = {'title': 'home', 'user': 'store', 'store_name': req.session.get('store_name')}
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
    else:
        store_id = req.session.get('store_id')
        # Checking if its a POST request and handle it.
        if req.method == 'POST':
            post = req.POST.copy()
            post['store_id'] = Store.objects.get(pk=req.session.get('store_id'))    # dbtrans
            form = AddproductForm(post, req.FILES)
            if form.is_valid():
                form.save()
                return redirect(home)
        else:
            form = AddproductForm()
        context = {'form': form, 'title': 'add product', 'store_id_id': store_id}
        return render(req, 'store/addproduct.html', context)
