from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.customer_registration_view, name='register'),
    path('login/', views.customer_login_view, name='login'),
    path('profile/', views.userprofile, name='profile'),
    path('profile/logout/', views.logout, name='logout'),
    path('<int:prod_id>/prod_details/',views.product_detail, name='prod_details'),
    path('<int:prod_id>/order/', views.order_view, name='order'),
]
