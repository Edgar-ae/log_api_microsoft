from django.urls import path
from . import views

urlpatterns = [
    path('', views.hello, name='n_home'),
    path('products/', views.products, name='n_products'),
]