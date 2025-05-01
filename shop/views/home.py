from django.shortcuts import render , redirect , HttpResponseRedirect
from shop.models.product import Product
from shop.models.models import *
from shop.models.category import Sub_Category
from shop.models.brand import Major_Categories
from shop.models.banner import Item
from django.views import View
from shop.models.orders import *
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import random
import requests
from .forms import *
# Create your views here.
class Index(View):

    def post(self , request):
        product = request.POST.get('product')
        remove = request.POST.get('remove')
        cart = request.session.get('cart')
        form=ViewCartForm()
         
        if request.method=='POST':
            if not cart:
                cart = {}
            if "quantity" in request.POST:  # Check if the request contains review data
                form = ViewCartForm(request.POST)
                print('we got the form')
                if form.is_valid():
                    print('form valid')
                    print(form.cleaned_data.get('quantity'))
                    if cart:
                        print(f'product:{product}')
                        cart[product]  =int(cart[product])+ form.cleaned_data.get('quantity')
                        print(cart[product])
                        print('What happened')
                    else:
                        cart = {}
                        print('did something happen')
                        cart[product]  = form.cleaned_data.get('quantity')
                    request.session['cart'] = cart
                    return redirect('details', product)
                else:
                    print("Form errors:", form.errors)


        elif cart:
            # comment:  cart:
            quantity = cart.get(product)
            if quantity:
                if remove:
                    if quantity<=1:
                        cart.pop(product)
                    else:
                        cart[product]  = quantity-1
                else:
                    cart[product]  = quantity+1

            else:
                cart[product] = 1
                print('added 1')
        else:
            print('is it entered')
            cart = {}
            cart[product] = 1

        request.session['cart'] = cart
        return redirect('home')



    def get(self , request):
        # print()
        return HttpResponseRedirect(f'/store{request.get_full_path()[1:]}')
def clearcart (request):
    cart = request.session.get('cart')
    request.session['cart'] = {}
    return redirect('store')
from django.core.paginator import Paginator
from django.shortcuts import render
from django.contrib import messages

def store(request):
    cart = request.session.get('cart', {})
    if not cart:
        request.session['cart'] = {}

    productes = Product.get_products_by_id(list(cart.keys())) if cart else {}

    categories = Sub_Category.get_all_categories()
    brands = Major_Categories.get_all_brand()
    categoryID = request.GET.get('category')
    brandID = request.GET.get('brand')
    customer = request.user.id
    k = request.GET.get('caution')

    if k:
        Order.objects.filter(id=k, customer=customer).delete()
        orders = Order.get_orders_by_customer(customer)
        messages.success(request, 'Order Item deleted Successfully')
        return render(request, 'orders.html', {'orders': orders})

    # Filter products based on category or brand
    if categoryID:
        products = Product.get_all_products_by_categoryid(categoryID)
    elif brandID:
        products = Product.objects.filter(category__brand_id=brandID)#Product.get_all_products_by_brandid(brandID)
    else:
        products = Product.objects.all().order_by('?')  # Random order

    # PAGINATION
    paginator = Paginator(products, 20)  # 20 items per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)  # Get the current page

    # Vendor presence check
    vendor_present_here = request.user.is_authenticated and Vendor.objects.filter(vendor=request.user.id).exists()
    if request.user.is_authenticated:
        user = request.user
        # Retrieve Like objects related to the current user, with their associated products.
        likes = Like.objects.filter(user=user).select_related('product')
        # Create a list of product objects that the user has liked.
        liked_products = [like.product.id for like in likes]
    else:
        liked_products=[]
    categories = Sub_Category.get_all_categories()
    brands = Major_Categories.get_all_brand()
    context = {
        
        'liked_products':liked_products,
        'page_obj': page_obj,  # Pass paginated products
        'vendor_present_here': vendor_present_here,
        'store': 'store',
        'products':productes,
        'k': categoryID or brandID,  # Preserve filter
        'brands': brands,
        'categories': categories,
        
    }

    return render(request, 'shop-grid.html', context)

def search(request): 
    cart = request.session.get('cart')
    if not cart:
        request.session['cart'] = {}
        productes={}
    else:
        productes = Product.get_products_by_id(list(request.session.get('cart').keys()))

    if request.user.is_authenticated:
        vendor_present=Vendor.objects.filter(vendor=request.user.id)
        vendor_present_here=True
    else:
        vendor_present_here=False
        
    if request.method=="POST":
        categories =Sub_Category.get_all_categories()
        brands = Major_Categories.get_all_brand()
        searched=request.POST['searched']
        try:
            multiple_q=Q(Q(name__icontains=searched) | Q(description__icontains=searched))
            page_obj=Product.objects.filter(multiple_q).order_by('?')
            '''random.shuffle(list(page_obj))
            paginator=Paginator(products,20)
            page_number=request.GET.get('page')
            page_obj = paginator.get_page(page_number)'''
        except:
            page_obj={}
        context={'page_obj':page_obj,'vendor_present_here':vendor_present_here,'store':'store','products':productes,'searched':searched,'brands':brands,'categories':categories}

        return render(request,'shop-grid.html', context)

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        # Handle multiple IPs in headers
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def my_view(request):
    
    return HttpResponse(f"Your IP: {user_ip}")


def homepage(request):
    cart = request.session.get('cart')
    items=Item.objects.all()
    user_ip = get_client_ip(request)
    print(f"User IP: {user_ip}")

    for item in items:
        item['description_words'] = item['description'].split()

    if not cart:
        request.session['cart'] = {}
        productes={}
    else:
        productes = Product.get_products_by_id(list(request.session.get('cart').keys()))
    products ={}
    categories = Sub_Category.get_all_categories()
    categoryID = request.GET.get('category')
    brands = Major_Categories.get_all_brand()
    brandID = request.GET.get('brand')

    if categoryID:
        products = Product.get_all_products_by_categoryid(categoryID)
    elif brandID:
        products = Product.get_all_products_by_brandid(brandID)

    else:
        products = Product.get_all_products();



    top_rated=list(Product.objects.filter(is_top_rated=True).order_by('-dates')[:12])
    latest_products=Product.objects.filter(is_featured=True).order_by('-dates')[:12]
    top_reviewed= list(Product.objects.filter(is_featured=True).order_by('-dates')[:12])
    category_products=list(Product.objects.all().order_by('-dates')[:30])

    top_rated=random.sample(top_rated, len(top_rated))
    #latest_products=random.sample(latest_products, len(latest_products))
    top_reviewed=random.sample(top_reviewed, len(top_reviewed))
    
    '''random.shuffle(list(top_rated))
    random.shuffle(list(featured))
    random.shuffle(list(best_selling))
    random.shuffle(list(new_arrival))
    random.shuffle(list(new_product))
    random.shuffle(list(hot_sale))
    random.shuffle(list(hot_sale))
    random.shuffle(list(hot_deal))
    random.shuffle(list(products))'''

    latest=Post.objects.order_by('-date_posted')[:5]
    news=Post.objects.all().order_by('-date_posted')[:3]
    '''
    #brands_display = Major_Categories.objects.prefetch_related('categories')  # Optimize query
    brands =  Major_Categories.objects.prefetch_related('categories').all()
    for brand in brands:
        for cat in brand.categories.all():
            # collect all product image URLs under this category
            urls = []
            for prod in Product.objects.filter(category=cat):
                for i in range(1, 2):  # or however many images per product
                    img = getattr(prod, f'image{i}', None)
                    if img and hasattr(img, 'url'):
                        urls.append(img.url)
            # attach to the category so the template can see it
            cat.carousel_images = urls
    '''
   
    chunked_products1 =[latest_products[i:i + 3] for i in range(0, len(latest_products), 3)]
    
    chunked_products2 = [top_rated[i:i + 3] for i in range(0, len(top_rated), 3)]
    
    chunked_products3 = [latest_products[i:i + 3] for i in range(0, len(latest_products), 3)]
    if request.user.is_authenticated:
        user = request.user
        # Retrieve Like objects related to the current user, with their associated products.
        likes = Like.objects.filter(user=user).select_related('product')
        # Create a list of product objects that the user has liked.
        liked_products = [like.product.id for like in likes]
    else:
        liked_products=[]

    context = {
        
        'category_products':category_products,'news':news,'liked_products':liked_products,'IP':user_ip,'items': items,"chunked_products1": chunked_products1,"chunked_products2": chunked_products2,"chunked_products3": chunked_products3,'homepage':'homepage','latest_products':latest_products,'top_reviewed':top_reviewed,'productes':productes,'products':products,'brands':brands,'categories':categories ,'top_rated':top_rated,}

    return render(request, 'index.html', context)




def error_404_view(request, exception):
    return render(request,'404.html')
