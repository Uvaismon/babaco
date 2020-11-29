from django.shortcuts import render, redirect
from django.http import HttpResponse
from shop.views import login_view, registration_view
from shop.models import Store, Product
from .forms import StoreRegistrationForm, AddproductForm
from django.contrib import messages


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
        return redirect(home)
    else:
        store_id = req.session.get('store_id')
         # Checking if its a POST request and handle it.
        if req.method == 'POST' :
            form = AddproductForm(req.POST)
            if form.is_valid():
                # form._mutable = True
                # passwd = sha256(form.cleaned_data['password'].encode()).hexdigest()
                # form.data['password'] = passwd
                # logging.debug(passwd)
                # logging.debug(form.cleaned_data['password'])
                form.save()
                return redirect(home)
            else:
                # Checking for errors in the form.
                if form.has_error('name'):
                    messages.error(req, 'Invalid name')
                elif form.has_error('details'):
                    messages.error(req, 'Please add the details correctly')
                elif form.has_error('price'):
                    messages.error(req, 'Invalid amount')
                elif form.has_error('image'):
                    messages.error(req, 'Invalid picture')
                elif form.has_error('category'):
                    messages.error(req, 'fill category')
        else:
            form = AddproductForm()
        context = {'form': form, 'title': 'add product',  'store_id_id': store_id}
        return render(req, 'store/addproduct.html', context)