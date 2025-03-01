from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("shop", views.shop, name="shop"),
    path("product", views.product_detail, name="product_detail"),
    path("contact", views.contact, name="contact"),
    path("checkout", views.checkout, name="checkout"),
    path("cart", views.cart, name="cart"),
]
