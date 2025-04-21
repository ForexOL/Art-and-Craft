from django.contrib.sitemaps import Sitemap
from django.urls import reverse
# yourapp/sitemaps.py
from shop.models.product import Product  

class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = 'monthly'

    def items(self):
        return ['signup','login','search','blog','home', 'about_us', 'Contact','return_policy','delivery_information','terms_and_conditions','privacy_policy']  # names of URL patterns

    def location(self, item):
        return reverse(item)



class ProductSitemap(Sitemap):
    changefreq = 'weekly'
    priority   = 0.8

    def items(self):
        qs = Product.objects.all()
        # If fewer than 50k, index all; otherwise only the latest 10
        #if qs.count() <= 50000:
        #    return qs
        return

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return obj.get_absolute_url()