from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import LoginForm


def registration_view(req, user, reg_form, ret):
    """General function to handle registration view."""

    if req.session.get(user + '_id'):
        return redirect(ret)

    # Checking if its a POST request and handle it.
    if req.method == 'POST':
        form = reg_form(req.POST)
        form.verify()
        if form.is_valid():
            form.save()  # dbtrans
            return redirect(ret)
        else:
            # Checking for errors in the form.
            if form.has_error('email'):
                messages.error(req, 'User with the given email already exists.')
            elif form.has_error('password'):
                messages.error(req, 'Password confirmation failed')
            elif form.has_error('name'):
                messages.error(req, 'Invalid name')
            elif form.has_error('contact'):
                messages.error(req, 'Invalid contact number.')
    else:
        form = reg_form()
    context = {'form': form, 'title': 'register', 'user': user, user + '_name': req.session.get(user + '_name')}
    return render(req, 'shop/registration.html', context)


def login_view(req, user, database, ret):
    # General function to handle login views.

    if req.session.get(user + '_id'):
        return redirect(ret)
    if req.method == 'POST':
        form = LoginForm(req.POST)

        if form.is_valid():
            # Retrieving form data.
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            # Checking against database data.
            if database.objects.filter(email=email):    # dbtrans
                x = database.objects.get(email=email)  # dbtrans
                if x.password != password:
                    form.add_error('password', 'Wrong Password')
            else:
                form.add_error('email', 'Email not registered')

        if form.is_valid():
            req.session[user + '_id'] = database.objects.get(email=email).user_id   # dbtrans
            req.session[user + '_name'] = database.objects.get(email=email).name    # dbtrans
            return redirect(ret)
        else:
            if form.has_error('email'):
                messages.error(req, 'The given email is not registered!')
            elif form.has_error('password'):
                messages.error(req, 'Incorrect Password')
    else:
        form = LoginForm()
    context = {'form': form, 'title': 'login', 'user': user, user + '_name': req.session.get(user + '_name')}
    return render(req, 'shop/login.html', context)


