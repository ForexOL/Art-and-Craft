from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from django.views import View
import random
from myshop_1 import settings
from shop.models.product import Product
from shop.models.orders import Order
from shop.models.models import *
from shop.models.brand import Major_Categories
from shop.models.category import Sub_Category
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
import datetime
from .forms import *
from django.utils import timezone
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse

now = timezone.now() # current date and time


time = now.strftime("%H:%M:%S")


date_time = now.strftime("%m/%d/%Y, %H:%M:%S")


 
@login_required(login_url='login')
def checkout(request):
    brands = Major_Categories.get_all_brand()
    address = request.POST.get('address')
    email = request.POST.get('email')
    phone = request.POST.get('phone')
    cart = request.session.get('cart')
    customer = request.user.id
    products = Product.get_products_by_id(list(cart.keys()))
    ordering_code= ''.join([random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ') for _ in range(3)])
    product_lists=""
    dates=datetime.datetime.today()

    if products:
        total_price=0
        for product in products:
            total_price=int(total_price)+int(product.price)
            
        brands = Major_Categories.get_all_brand()
        categories =Sub_Category.get_all_categories()

        context={'product_lists':product_lists,'categories':categories,'brands':brands}
        if request.method=='POST':
            total_price=total_price+3000
            order = Order.objects.create(customer=request.user,ordering_code=ordering_code,total_price=total_price)
            
            request.session['ordering_code'] = f'{ordering_code}'
            ordered_products = [
                Order_record(
                    order=order,
                    name=prod.name,
                    quantity=cart.get(str(product.id)),  # or whichever field holds the quantity
                    price=prod.price         # or the correct field name
                )
                for prod in products
            ]
            
            Order_record.objects.bulk_create(ordered_products)
            request.session['cart'] = {}
            return redirect('payment')
        return render(request, 'success.html',context)
    else:
        messages.success(request, f'You Have an empty Cart, Please Add Orders to Cart and Make Your Order')
        return redirect('checkout1')

import math,requests

def process_payment(name,email,amount,phone,ordering_code):
     auth_token= 'FLWSECK_TEST-9d95ef51f2cff0ee18cb3377923e8095-X'
     request.session['cart'] = {}
     hed = {'Authorization': 'Bearer ' + auth_token}
     data = {
                "tx_ref":ordering_code,
                "amount":amount,
                "currency":"UGX",

                "redirect_url":"http://localhost:8000/callback",
                "payment_options":"mobilemoneyuganda",
                "meta":{
                    "consumer_id":23,
                    "consumer_mac":"92a3-912ba-1192a"
                },
                "customer":{
                    "email":email,
                    "phonenumber":phone,
                    "name":name
                },
                "customizations":{
                    "title":"Pearlmart",
                    "description":"Your loyal online Market",
                    "logo":"https://getbootstrap.com/docs/4.0/assets/brand/bootstrap-solid.svg"
                }
                }
     url = ' https://api.flutterwave.com/v3/payments'
     response = requests.post(url, json=data, headers=hed)
     response=response.json()
     link=response['data']['link']
     return link

def process_payment_visa(name,email,amount,phone,ordering_code):
     auth_token= 'FLWSECK_TEST-9d95ef51f2cff0ee18cb3377923e8095-X'
     request.session['cart'] = {}
     hed = {'Authorization': 'Bearer ' + auth_token}
     data = {
                "tx_ref":ordering_code,
                "amount":amount,
                "currency":"UGX",

                "redirect_url":"http://localhost:8000/callback",
                "payment_options":"card",
                "meta":{
                    "consumer_id":23,
                    "consumer_mac":"92a3-912ba-1192a"
                },
                "customer":{
                    "email":email,
                    "phonenumber":phone,
                    "name":name
                },
                "customizations":{
                    "title":"Pearlmart",
                    "description":"Your loyal online Market",
                    "logo":"https://getbootstrap.com/docs/4.0/assets/brand/bootstrap-solid.svg"
                }
                }
     url = ' https://api.flutterwave.com/v3/payments'
     response = requests.post(url, json=data, headers=hed)
     response=response.json()
     link=response['data']['link']
     return link


@require_http_methods(['GET', 'POST'])
def payment_response(request):
    status=request.GET.get('status', None)
    tx_ref=request.GET.get('tx_ref', None)
    if status==SUCCESSFUL:
        messages.success(request, 'Verified Successful')
    else:
        messages.error(request, 'Verified Failed')
    print(status)
    print(tx_ref)
    return HttpResponse('Finished')
