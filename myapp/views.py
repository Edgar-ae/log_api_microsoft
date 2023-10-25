from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

# Create your views here.
def hello(request):
    return render(request,'home.html')

@login_required
def products(request):
    return render(request,'productos.html')
