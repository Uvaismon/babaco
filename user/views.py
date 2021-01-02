from django.shortcuts import render, redirect
import datetime
from babaco import settings
from shop.views import registration_view, login_view
from .forms import CustomerRegistrationForm, OrderForm, ReviewForm
from shop.models import Customer, Product, Store, Order, Review, Category
from django.core.paginator import Paginator
from django.http import HttpResponseForbidden


def home(req):
    message = None
    home = True
    if req.method == 'POST':
        home = False
        products = Product.objects.filter(name__icontains=req.POST['search']) or \
                   Product.objects.filter(details__icontains=req.POST['search'])  # dbtrans
    else:
        products = Product.objects.all()[::-1]  # dbtrans
        products = products[:8]
    if len(products) == 0:
        message = "No result found!"
    context = {'title': 'home', 'user': 'user', 'user_name': req.session.get('user_name'), 'message': message,
               'products': products, 'categories': Category.objects.all(), 'home': home}
    return render(req, 'user/home.html', context)


def customer_registration_view(req):
    """Function to handle customer registration view."""
    return registration_view(req, user='user', reg_form=CustomerRegistrationForm, ret='login')


def customer_login_view(req):
    """Class to handle Customer login view."""
    return login_view(req, user='user', database=Customer, ret='home')


def userprofile(req):
    if req.method == 'POST':
        cust_id = Customer.objects.get(pk=req.session.get('user_id'))  # dbtrans
        cust_id.delete()
        req.session.flush()
        return redirect('home')

    if req.session.get('user_id'):
        customer_id = Customer.objects.get(pk=req.session.get('user_id'))  # dbtrans
        context = {'customer_id': customer_id, 'title': 'profile', 'user': 'user'}
        return render(req, 'user/userprofile.html', context)
    else:
        return redirect('login/')


def product_detail(req, prod_id):
    if req.method == 'POST':
        rev_id = int(req.POST.get('rev_id'))
        rev = Review.objects.get(pk=rev_id)
        if rev.cust_id.user_id != req.session.get('user_id'):
            return HttpResponseForbidden()
        rev.delete()

    product_name = Product.objects.get(prod_id=prod_id)
    store_id = product_name.store_id
    reviews = Review.objects.filter(prod_id=product_name)
    if len(reviews) == 0:
        reviews = None
    context = {'prod_name': product_name, 'title': product_name.name, 'store_id': store_id, 'user': 'user',
               'user_name': req.session.get('user_name'), 'reviews': reviews, 'user_id': req.session.get('user_id')}
    return render(req, 'user/product_details.html', context)


def logout(req):
    req.session.flush()
    return redirect('home')


def order_view(req, prod_id):
    if not req.session.get('user_id'):
        return redirect(customer_login_view)

        # Checking if its a POST request and handle it.
    product = Product.objects.get(pk=prod_id)  # dbtrans
    if req.method == 'POST':
        post = req.POST.copy()
        cust = Customer.objects.get(pk=req.session.get('user_id'))  # dbtrans
        post['cust_id'] = cust
        post['prod_id'] = product
        post['date'] = datetime.date.today()
        form = OrderForm(post)
        if form.is_valid():
            form.save()
            return redirect(home)
    else:
        form = OrderForm()
    context = {'user': 'user', 'title': 'order', 'product': product, 'form': form,
               'user_id': req.session.get('user_id'), 'user_name': req.session.get('user_name')}
    return render(req, 'user/order_user.html', context)


def review_view(req, prod_id):
    if not req.session.get('user_id'):
        return redirect(customer_login_view)
    product = Product.objects.get(pk=prod_id)
    user = Customer.objects.get(pk=req.session.get('user_id'))
    if req.method == "POST":
        post = req.POST.copy()
        post['cust_id'] = user
        post['prod_id'] = product
        post['date'] = datetime.date.today()
        form = ReviewForm(post)
        if form.is_valid():
            form.save()
            return redirect(product_detail, prod_id=prod_id)
    form = ReviewForm()
    context = {'user': 'user', 'user_name': req.session.get('user_name'), 'product': product, 'cust': user,
               'title': 'product review', 'form': form}
    return render(req, 'user/review.html', context)


def filtered_view(req, cat_id=-1):
    if req.method == 'POST':
        return home(req)

    message = None
    if cat_id == -1:
        products = Product.objects.all()
    else:
        products = Product.objects.filter(category=cat_id)
    if len(products) == 0:
        message = "No result found!"
    context = {'title': 'home', 'user': 'user', 'user_name': req.session.get('user_name'), 'message': message,
               'products': products,
               'categories': Category.objects.all(), 'search_bar': None}
    return render(req, 'user/home.html', context)


def filtered_view_all(req):
    return filtered_view(req)


def myorders_view(req):
    if req.session.get('user_id'):
        products = Order.objects.filter(cust_id=req.session.get('user_id'))  # dbtrans

        if products:
            paginator = Paginator(products, 2)
            page = req.GET.get('page')
            products = paginator.get_page(page)
            context = {'products': products, 'title': 'orders', 'user': 'user',
                       'user_name': req.session.get('user_name')}
            return render(req, 'user/orders.html', context)
        else:
            context = {'products': 'zero', 'title': 'orders', 'user': 'user', 'user_name': req.session.get('user_name')}
            return render(req, 'user/orders.html', context)

    else:
        return redirect('login')
