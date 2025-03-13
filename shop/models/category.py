from django.db import  models
from django.contrib.auth.models import User
from .brand import *


class Sub_Category(models.Model):
    name = models.CharField(max_length=45)
    shop =models.CharField(max_length=100,default=1,blank=True)
    brand = models.ForeignKey(Major_Categories, on_delete=models.CASCADE, related_name='categories', null=True)
    image =models.ImageField(upload_to='Categories/', blank=True, null=True, default='Categories/arcrid.jpg')
    is_tech=models.BooleanField(default=False)
    is_fashion=models.BooleanField(default=False)
    is_home=models.BooleanField(default=False)
    is_party=models.BooleanField(default=False)
    is_tagged=models.BooleanField(default=False)
    @staticmethod
    def get_all_categories():
        return Sub_Category.objects.all()


    def __str__(self):
        return f"{self.brand.name} - {self.name}"
