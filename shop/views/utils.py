# payments/utils.py
from django.urls import reverse
from django_pesapalv3.views import PaymentRequestMixin
from shop.models.orders import *

# payments/utils.py


def get_pesapal_payment_iframe(request, ordering_code: str):
    """
    Authenticates with Pesapal and returns the redirect URL for the payment iframe.

    :param request: Django HttpRequest (for user info)
    :param ordering_code: the Order.ordering_code to charge
    """
    if not ordering_code:
        raise ValueError("ordering_code must be provided")

    # 1. Create a fresh mixin instance and bind the request
    pesapal = PaymentRequestMixin()
    pesapal.request = request

    # 2. Notification/IPN token
    ipn = pesapal.get_default_ipn()

    # 3. Fetch the Order
    try:
        order = Order.objects.get(ordering_code=ordering_code)
    except Order.DoesNotExist:
        raise ValueError(f"Order with code {ordering_code!r} not found")

    # 4. Build Pesapal order payload
    order_info = {
        "id": ordering_code,
        "currency": "UGX",
        "amount": int(order.total_price),
        "description": f"Payment for Order Code: {ordering_code}",
        # build_url now uses pesapal.request internally
        "callback_url": pesapal.build_url(reverse("pesapal_callback")),
        "notification_id": ipn,
        "billing_address": {
            "first_name": request.user.username,
            "last_name": "",
            "email": request.user.email,
        },
    }

    # 5. Submit to Pesapal and pull out the redirect_url
    resp = pesapal.submit_order_request(**order_info)
    return resp.get("redirect_url", "")
