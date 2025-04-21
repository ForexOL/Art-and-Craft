from django.shortcuts import render , redirect , HttpResponseRedirect, HttpResponse
from django.contrib.auth.hashers import  check_password
from django.views import  View
from shop.models.product import *
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .home import Index,store
from django.contrib.auth import authenticate, login, logout
from .viewproduct import checkout1
from django.contrib import messages
from .forms import LoginForm

def Login(request):

    cart = request.session.get('cart')
    if not cart:
        request.session['cart'] = {}
        productes={}
    else:
        productes = Product.get_products_by_id(list(request.session.get('cart').keys()))
    if request.method=='POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data['username']
            password=form.cleaned_data['password']
            print('here')
            user=authenticate(request, username=username,password=password)

            if user is not None:
                login(request,user)
                request.session['customer'] = user.id
                if 'next' in request.POST:
                    return redirect(request.POST['next'])
                else:
                    messages.success(request, f'Welcome, {username}.You have Signed In Successfully')
                    return redirect('store')
            else:
                messages.success(request, 'Username or Password Incorrect!')
                context={'productes':productes}
                return render(request,'Vender/login.html',context)
        else:
            print(form.errors)
            return HttpResponse(f'form is invalid: {form.errors}')
    brands = Major_Categories.get_all_brand()
    categories =Sub_Category.get_all_categories()
    form = LoginForm()
    
    context={'productes':productes,'brands':brands,'categories':categories, 'form':form}
    return render(request,'Vender/login.html',context)


@login_required(login_url='login')
def Logout(request):
    logout(request)
    messages.success(request, 'You have Signed Out Successfully')
    return redirect('store')
 