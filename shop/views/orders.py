from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password
from django.views import View
from shop.models.product import Product
from shop.models.brand import *
from shop.models.category import *
from shop.models.orders import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required(login_url='login')
def delete(request, id):
    if request.method=='POST':
        order=Order.objects.filter(id=id)
        order.delete()
        return redirect('orders')



    

@login_required(login_url='login')
def orders(request):
    brands = Major_Categories.get_all_brand()
    categories =Sub_Category.get_all_categories()
    cart = request.session.get('cart')
    if not cart:
        request.session['cart'] = {}
        productes={}
    else:
        productes = Product.get_products_by_id(list(request.session.get('cart').keys()))
    orders = Order.get_orders_by_customer(request.user.id)
    deleteorder=request.GET.get('order')
    order = request.POST.get('order')
    if deleteorder:
        order=Order.objects.filter(id__in=deleteorder)
        order_record=Order_record.objects.filter(quantity=order.quantity).filter(ordering_code=order.ordering_code).filter(product=order.product.name)
        try:
            product_stock=Product.objects.filter(name=order.product.name).filter(shop_name=order.shop_name).filter(id=order.product.id)
            product_stock.stock=(product_stock.stock+order.quantity)
            product_stock.save()
        except:
            pass
        order_record.delete()
        order.delete()
        messages.success(request, f'Order for {order}Item Cancelled Successfully')
    print(orders)
    
    
    return render(request , 'orders.html'  , {'orders' : orders,'orderes':'orderes','productes':productes,'brands':brands,'categories':categories})