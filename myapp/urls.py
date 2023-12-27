from django.urls import path
from . import views

urlpatterns = [
    path('', views.hello, name='n_home'),
    path('init/', views.products, name='n_products'),
    path('logout/', views.exit, name='n_exit'),
]