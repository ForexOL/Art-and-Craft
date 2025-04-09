# payments/views.py

import uuid
from django.views.generic import TemplateView
from django.urls import reverse
import requests
from shop.models.orders import *
from django_pesapalv3.views import PaymentRequestMixin
class PaymentView(PaymentRequestMixin, TemplateView):
    template_name = 'payments/payment.html'

    def get_pesapal_payment_iframe(self):
        """
        Authenticates with Pesapal to get the payment iframe src.
        """
        ipn = self.get_default_ipn()
        ordering_code = str(self.request.session.get('ordering_code'))
        print(ordering_code)
        #total_price=10000
        
        order = Order.objects.get(ordering_code=ordering_code)
        print(order.customer)
        print(ordering_code,type(order.total_price))
        
        number=int(order.total_price)
        order_info = {
            "id": self.request.GET.get("id", uuid.uuid4().hex),  # Replace with a valid merchant id if needed.
            "currency": "UGX",
            "amount":number,
            "description": "Payment for X",
            "callback_url": self.build_url(
                reverse("pesapal_callback")
            ),
            "notification_id": ipn,
            "billing_address": {
                "first_name": "John",
                "last_name": "Doe",
                "email": "pesapal@example.com",
            },
        }
        print(order_info)
        req = self.submit_order_request(**order_info)
        return req.get("redirect_url", "")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['iframe_src_url'] = self.get_pesapal_payment_iframe()
        return context

from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse


class OrderHistoryView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'order_history.html'
    context_object_name = 'orders'
    
    def get_queryset(self):
        # Display current user's orders, sorted with latest first.
        return Order.objects.filter(customer=self.request.user).order_by('-dates')

def pesapal_callback(request):
    """
    View to handle Pesapal callback.
    We assume the Pesapal callback sends the ordering code as a GET parameter (or you can adjust as needed).
    """
    ordering_code = request.GET.get('id')  # adjust the parameter name as needed
    if ordering_code:
        order = get_object_or_404(Order, ordering_code=ordering_code)
        # Update the order status if payment was successful.
        # You might want to check additional parameters or IPN signals here.
        order.status = True
        order.save()
    # Redirect to the order history page
    return redirect(reverse('order_history'))
