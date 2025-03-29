from django.db import models
from .product import Product
from .models import *
from django.contrib.auth.models import User
import datetime


class Order(models.Model):
    customer = models.ForeignKey(User,
                                 on_delete=models.CASCADE)
    total_price = models.IntegerField(default=0)
    status = models.BooleanField(default=False)
    ordering_code=models.CharField(max_length=60,default='')
    address=models.CharField(max_length=100,default='')
    phone=models.CharField(max_length=60,default='')
    dates = models.DateTimeField(auto_now_add=True)

    def placeOrder(self):
        self.save()



    @staticmethod
    def get_by_id(id):
        if category_id:
            return Order.objects.filter(id=id).order_by('?')
        else:
            return None




    @staticmethod
    def get_orders_by_customer(customer_id):
        return Order.objects.filter(customer=customer_id).order_by('-dates')


