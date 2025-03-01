from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return render(request, 'index.html')

def shop(request):
    return render(request, 'shop-grid.html')

def product_detail(request):
    return render(request, 'shop-details.html')

def contact(request):
    return render(request, 'contact.html')

def checkout(request):
    return render(request, 'checkout.html')

def cart(request):
    return render(request, 'shoping-cart.html')
