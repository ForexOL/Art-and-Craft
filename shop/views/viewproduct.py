from django.shortcuts import render , redirect
from django.contrib.auth.hashers import  check_password
from django.views import  View
from shop.models.product import  Product
from shop.models.category  import Sub_Category 
from shop.models.brand import  Major_Categories
from .forms import *#OrderForm,ViewCartForm,PaymentForm
from django.contrib.auth.decorators import login_required
from shop.middlewares.auth import auth_middleware
import random 

def lart(request):
    brands = Major_Categories.get_all_brand()
    categories =Sub_Category.get_all_categories()
    cart = request.session.get('cart')

    
    
    if not cart:
        request.session['cart'] = {}
        productes={}
        products={}
    else:
        productes = Product.get_products_by_id(list(request.session.get('cart').keys()))
        products = Product.get_products_by_id(list(request.session.get('cart').keys()))

    return render(request , 'cart.html' , {'products':products,'productes' : productes,'brands':brands,'categories':categories} )



def details(request, id):
    brands = Major_Categories.get_all_brand()
    categories =Sub_Category.get_all_categories()
    cart = request.session.get('cart')

    

    if not cart:
        request.session['cart'] = {}
        productes={}
    else:
        productes = Product.get_products_by_id(list(request.session.get('cart').keys()))
    form=ViewCartForm()
    '''
    if request.method=='POST':
        product = request.POST.get('product')
        cart = request.session.get('cart')
        quantitey = cart.get(product)
        form=ViewCartForm(request.POST)
        if form.is_valid():
            cart[product] = form.cleaned_data.get('quantity')
    '''
    
    if request.method=='POST':
        if "rating" in request.POST:  # Check if the request contains review data
            review_form = ReviewForm(request.POST)
            if review_form.is_valid():
                review = review_form.save(commit=False)
                review.product = product
                review.user = request.user
                review.save()
                product.update_rating()
                return redirect("details", product_id=product.id)

        elif "quantity" in request.POST:  # Check if the request contains cart data
            
            product = request.POST.get('product')
            '''
            cart = request.session.get('cart')
            quantitey = cart.get(product)
            '''
            form=ViewCartForm(request.POST)
            print('Cart reached')
            if form.is_valid():
                print('Form valid')
                print(form.cleaned_data.get('quantity'))
                print(cart[product])
                cart[product] = form.cleaned_data.get('quantity')
            

    product=Product.objects.get(id=id)
    reviews = product.reviews.all()
    form_r = ReviewForm()
    related_products = list(Product.objects.filter(category=product.category.id).exclude(id=product.id))
    related_products=random.sample(related_products, len(related_products))
    k=random.randint(1, 25)
    G=random.randint(1, 20)

    context={'k':k,'G':G, "reviews": reviews, "form_r": form_r,'related_products': related_products,'product':product,'form':form,'productes':productes,'brands':brands,'categories':categories}    
    

    return render(request , 'shop-details.html',context)

#@login_required(login_url='login')
def checkout1(request):
    cart = request.session.get('cart')

    
    
    if not cart:
        request.session['cart'] = {}
        productes={}
        products={}
    else:
        productes = Product.get_products_by_id(list(request.session.get('cart').keys()))
        products = Product.get_products_by_id(list(request.session.get('cart').keys()))
    categories =Sub_Category.get_all_categories()
    categoryID = request.GET.get('category')
    brands = Major_Categories.get_all_brand()
    brandID = request.GET.get('brand')
    form=PaymentForm()
    if request.method=='POST':
        if categoryID:
            products = Product.get_all_products_by_categoryid(categoryID)
        elif brandID:
            products = Product.get_all_products_by_brandid(brandID)
        paginator=Paginator(products,30)
        page_number=request.GET.get('page')
    
    

        print(page_number)
        product_list = paginator.get_page(page_number)
        return render(request , 'index.html',{'product_list' : product_list,'categories':categories,'brands':brands,'products':products,'productes' : productes,})
    return render(request , 'checkout.html',{'form':form,'checkout':'checkout','categories':categories,'brands':brands,'products':products,'productes' : productes,})

def remove_to_cart(request):
    product = request.POST.get('product')
    cart = request.session.get('cart')
    cart.pop(product)

    request.session['cart'] = cart
    print('cart' , request.session['cart'])
    return redirect('lart')

def remove_to_store(request):
    product = request.POST.get('product')
    cart = request.session.get('cart')
    cart.pop(product)

    request.session['cart'] = cart
    print('cart' , request.session['cart'])
    return redirect('store')
    
def remove_to_checkout(request):
    product = request.POST.get('product')
    cart = request.session.get('cart')
    cart.pop(product)

    request.session['cart'] = cart
    print('cart' , request.session['cart'])
    return redirect('checkout1')
def remove_to_homepage(request):
    product = request.POST.get('product')
    cart = request.session.get('cart')
    cart.pop(product)

    request.session['cart'] = cart
    print('cart' , request.session['cart'])
    return redirect('homepage')
def remove_to_orders(request):
    product = request.POST.get('product')
    cart = request.session.get('cart')
    cart.pop(product)

    request.session['cart'] = cart
    print('cart' , request.session['cart'])
    return redirect('orders')






