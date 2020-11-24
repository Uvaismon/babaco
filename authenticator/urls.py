from django.urls import path
from . import views


urlpatterns = [
    path('/register', views.RegistrationView.customer_registration_view, name='register' ),
    path('/register/store', views.RegistrationView.store_registration_view, name='register.store'),
]