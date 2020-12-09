from django.shortcuts import render, redirect
import datetime
from babaco import settings
from shop.views import registration_view, login_view
from .forms import CustomerRegistrationForm, OrderForm
from shop.models import Customer, Product, Store, Order


def home(req):
    message = None
    if req.method == 'POST':
        products = Product.objects.filter(name__icontains=req.POST['search']) or \
                   Product.objects.filter(details__icontains=req.POST['search'])                               # dbtrans
    else:
        products = Product.objects.all()[:12]  # dbtrans
    if len(products) == 0:
        message = "No Product matching the result."
    context = {'title': 'home', 'user': 'user', 'user_name': req.session.get('user_name'), 'message': message,
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
        customer_id = Customer.objects.get(pk=req.session.get('user_id'))                                      # dbtrans
        context = {'customer_id': customer_id, 'title': 'profile'}
        return render(req, 'user/userprofile.html', context)
    else:
        return redirect('login/')


def product_detail(req, prod_id):
    product_name = Product.objects.get(prod_id=prod_id)
    store_id = product_name.store_id
    context = {'prod_name': product_name, 'media_url': settings.MEDIA_URL, 'title': product_name.name,
               'store_id': store_id, 'user': 'user', 'user_name': req.session.get('user_name')}
    return render(req, 'user/product_details.html', context)


def logout(req):
    req.session.flush()
    return redirect('home')


def order_view(req, prod_id):
    if not req.session.get('user_id'):
        return redirect(customer_login_view)

        # Checking if its a POST request and handle it.
    product = Product.objects.get(pk=prod_id)                                                                  # dbtrans
    if req.method == 'POST':
        post = req.POST.copy()
        cust = Customer.objects.get(pk=req.session.get('user_id'))                                             # dbtrans
        post['cust_id'] = cust
        post['prod_id'] = product
        post['date'] = datetime.date.today()
        form = OrderForm(post, req.FILES)
        if form.is_valid():
            form.save()
            return redirect(home)
    else:
        form = OrderForm()
    context = {'user': 'user', 'title': 'order', 'product': product, 'form': form,
               'user_id': req.session.get('user_id'), 'user_name': req.session.get('user_name')}
    return render(req, 'user/order_user.html', context)
