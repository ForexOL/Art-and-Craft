from django.db import models
from .category import Sub_Category
from .brand import Major_Categories
import datetime
from django.utils import timezone
from django.urls import reverse
from django.conf import settings
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

class Product(models.Model):
    name = models.CharField(max_length=50)
    price = models.IntegerField(default=0)
    del_price= models.IntegerField(default=0)
    selling_price =models.IntegerField(default=0)
    stock = models.IntegerField(default=0)
    category =models.ForeignKey(Sub_Category, on_delete=models.CASCADE, default=1)
    brand = models.ForeignKey(Major_Categories, on_delete=models.CASCADE, default=1)
    description = models.TextField(max_length=1000,blank=True,null=True)
    image =models.ImageField(upload_to='Uploads/products/', blank=False)
    #image=CloudinaryField('image')
    shop=models.CharField(max_length=100,default=1)
    shop_name =models.CharField(max_length=100,default='Pearlmart',blank=True)
    dates= models.DateTimeField(default=timezone.now)
    average_rating = models.FloatField(default=0.0)

    def update_rating(self):
        reviews = self.reviews.all()
        if reviews:
            self.average_rating = sum(r.rating for r in reviews) / len(reviews)
            self.save()


    @staticmethod
    def get_products_by_id(ids):
        return Product.objects.filter(id__in =ids).order_by('-id')


    @staticmethod
    def get_product_by_id(id):
        return Product.objects.filter(id__in =id).order_by('?')







    @staticmethod
    def get_all_products():
        return Product.objects.all().order_by('?')

    @staticmethod
    def get_all_products_by_categoryid(category_id):
        if category_id:
            return Product.objects.filter(category = category_id).order_by('?')
        else:
            return Product.objects.all().order_by('?');


    @staticmethod
    def get_all_products_by_brandid(brand_id):
        if brand_id:
            return Product.objects.filter(brand = brand_id).order_by('?')
        else:
            return Product.objects.all().order_by('?');


    @staticmethod
    def get_all_product():
        return Product.objects.all().order_by('?')

    def __str__(self):
    
        return self.name


    

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])  # 1 to 5 stars
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)