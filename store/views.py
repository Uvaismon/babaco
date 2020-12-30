from django.core.paginator import Paginator
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect
from shop.tests import logging
from shop.models import Store, Product, Order
from shop.views import login_view, registration_view
from .forms import StoreRegistrationForm, AddproductForm
from babaco.settings import firebase_storage


def home(req):
    if not req.session.get('store_id'):
        return redirect(store_login_view)
    store = Store.objects.get(pk=req.session.get('store_id'))  # db trans
    products = Product.objects.filter(store_id=store)  # db trans
    context = {'title': 'home', 'user': 'store', 'store_name': req.session.get('store_name'),
               'products': products}
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
        post['store_id'] = Store.objects.get(pk=store_id)  # dbtrans
        form = AddproductForm(post, req.FILES)
        if form.is_valid():
            mod = form.save()
            mod.imageUrl = firebase_storage.child(str(mod.image)).get_url(None)
            mod.save()
            return redirect(home)
    else:
        form = AddproductForm()
    context = {'form': form, 'title': 'add product', 'store_name': req.session.get('store_name'), 'mode': 'Add'}
    return render(req, 'store/addproduct.html', context)


def profile(req):
    if req.method == 'POST':
        store_id = Store.objects.get(pk=req.session.get('store_id'))  # dbtrans
        store_id.delete()
        req.session.flush()
        return redirect('home')
    if req.session.get('store_id'):
        store_id = Store.objects.get(pk=req.session.get('store_id'))  # dbtrans
        context = {'store_id': store_id, 'title': 'profile', 'user': 'store',
                   'store_name': req.session.get('store_name')}
        return render(req, 'store/profile.html', context)
    else:
        return redirect(login_view)


def orders_view(req):
    if req.session.get('store_id'):
        store_id = Store.objects.get(pk=req.session.get('store_id'))  # dbtrans
        products = Order.objects.all()
        storeorder_id = []

        if req.method == 'POST':
            order_id = req.POST['order_id']
            order = Order.objects.get(pk=order_id)
            order.delivered = True
            order.save()

        for product in products:
            order_id = product.order_id
            prod_id = product.prod_id
            if prod_id.store_id == store_id:
                order_details = Order.objects.get(order_id=order_id)  # dbtrans
                storeorder_id.append(order_details)
        try:
            print(storeorder_id[0])
            paginator = Paginator(storeorder_id, 2)
            page = req.GET.get('page')
            storeorder_id = paginator.get_page(page)
            context = {'order_details': storeorder_id, 'title': 'orders'}
            return render(req, 'store/storeorders.html', context)

        except:
            context = {'order_details': 'zero', 'title': 'orders'}
            return render(req, 'store/storeorders.html', context)
    else:
        return redirect('store/login/')


def logout(req):
    req.session.flush()
    return redirect('home')


def edit_product(req, prod_id):
    if not req.session.get('store_id'):
        return redirect(store_login_view)
    prod = Product.objects.get(pk=prod_id)
    if prod.store_id.user_id != req.session.get('store_id'):
        return HttpResponseForbidden()
    if req.method == 'POST':
        if req.POST.get('mode') == 'edit':
            post = req.POST.copy()
            post['store_id'] = req.session.get('store_id')
            form = AddproductForm(post, instance=prod)
            if form.is_valid():
                mod = form.save()
                mod.imageUrl = firebase_storage.child(str(mod.image)).get_url(None)
                mod.save()
                return redirect(home)
        elif req.POST.get('mode') == 'delete':
            prod.delete()
            return redirect(home)
    form = AddproductForm(instance=prod)
    context = {'form': form, 'title': 'edit-product', 'user': 'store', 'store_name': req.session.get('store_name'),
               'mode': 'Edit'}
    return render(req, 'store/editProduct.html', context)
