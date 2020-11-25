from django.shortcuts import render, redirect
from .forms import CustomerRegistrationForm, StoreRegistrationForm, LoginForm
from django.contrib import messages
from store.models import Store,Customer
from hashlib import sha256
import logging
logging.basicConfig(level='DEBUG', filename='debug.log')


class RegistrationView:

    @staticmethod
    def registration_view(req, usr):
        if usr == 'cust':
            reg_form = CustomerRegistrationForm
        elif usr == 'store':
            reg_form = StoreRegistrationForm
        else:
            raise Exception("usr Error: User mode not specified")

        if req.method == 'POST':
            form = reg_form(req.POST)
            form.verify()
            if form.is_valid():
                # form._mutable = True
                # passwd = sha256(form.cleaned_data['password'].encode()).hexdigest()
                # form.data['password'] = passwd
                # logging.debug(passwd)
                # logging.debug(form.cleaned_data['password'])

                form.save()
                return redirect('home')
            else:
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
        return render(req, 'authenticator/registration.html', {'form': form, 'title': 'register', 'usr': usr})

    @staticmethod
    def customer_registration_view(req):
        return RegistrationView.registration_view(req, usr='cust')

    @staticmethod
    def store_registration_view(req):
        return RegistrationView.registration_view(req, usr='store')

class LoginView:

    @staticmethod
    def login_view(req, usr):
        login_form = LoginForm
        '''if usr == 'cust':
            user = 'cust'
        elif usr == 'store':
            user = 'store'
        else:
            raise Exception("usr Error: User mode not specified")'''

        if req.method == 'POST':
            form = login_form(req.POST)

            if form.is_valid():
                email = form.cleaned_data['email']
                password = form.cleaned_data['password']
                if usr == 'store':
                    z = Store
                else:
                    z = Customer
                if z.objects.filter(email=email):
                    x = z.objects.get(email=email)
                    if x.password == password:
                        pass
                    else:
                        form.add_error('password', 'Wrong Password')
                else:
                    form.add_error('email', 'Email not registered')

            if form.is_valid():
                return redirect('home')
            else:
                if form.has_error('email'):
                    messages.error(req, 'Account with this email is not registered! Please create an account.')
                elif form.has_error('password'):
                    messages.error(req, 'Incorrect Password')
                '''elif form.has_error('name'):
                    messages.error(req, 'Invalid name')
                elif form.has_error('contact'):
                    messages.error(req, 'Invalid contact number.')'''
        else:
            form = login_form()
        return render(req, 'authenticator/login.html', {'form': form, 'title': 'login', 'usr': usr})

    @staticmethod
    def customer_login_view(req):
        return LoginView.login_view(req, usr='cust')

    @staticmethod
    def store_login_view(req):
        return LoginView.login_view(req, usr='store')
