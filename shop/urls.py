from django.urls import path, include
from . import views


urlpatterns = [
    path('', include('user.urls')),
    path('store/', include('store.urls')),
    path('logout/', views.logout, name='logout'),
]