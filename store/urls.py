from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home.store'),
    path('register/', views.store_registration_view, name='register.store'),
    path('login/', views.store_login_view, name='login.store'),
    path('addproduct/', views.store_addproduct_view, name='addproduct.store'),
    path('profile/', views.profile, name='profile.store'),
    path('profile/logout/', views.logout, name='logout.store'),
    path('orders/',views.orders_view, name='orders.store'),
]
