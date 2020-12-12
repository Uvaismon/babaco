from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.customer_registration_view, name='register'),
    path('login/', views.customer_login_view, name='login'),
    path('profile/', views.userprofile, name='profile'),
    path('profile/logout/', views.logout, name='logout'),
    path('<int:prod_id>/prod_details/', views.product_detail, name='prod_details'),
    path('<int:prod_id>/order/', views.order_view, name='order'),
    path('<int:prod_id>/review/', views.review_view, name='review'),
    path('<int:cat_id>/view', views.filtered_view, name='filtered_view'),
    path('view', views.filtered_view_all, name='filtered_view_all'),
    path('orders/', views.myorders_view,name='My orders')
]
