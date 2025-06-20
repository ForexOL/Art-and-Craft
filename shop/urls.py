from django.urls import path
from shop.views.views import *
from shop.views import views
from django.contrib import admin
from django.urls import path
from .views.home import Index , store,search,homepage,clearcart
from .views.signup import signup
from .views.auction import *
from .views.coinbasecommerce import *
from .views.login import Login , Logout
from .views.viewproduct import *
from .views.checkout import checkout,payment_response
from .views.orders import orders,delete
from .views.payments import *
from .middlewares.auth import  auth_middleware
from django.contrib.auth import views as auth_views
from .views.payments import *
from shop.graph import *


urlpatterns = [
    #Flutterwave
    path('callback', payment_response, name='payment_response'),
    #path('<str:ref>', views.verifypayment, name='verifypayment'),
    #Auction Room
    path('auctionroom', auctionroom, name='auctionroom'),

    #Coinbase commerce
    path('home_view', home_view, name='home_view'),
    path('success', success_view, name='payments-success'),
    path('cancel', cancel_view, name='payments-cancel'),
    path('webhook', coinbase_webhook),

    #Graph Urls
    path('chartJSON_Asset', line_chart_json_asset, name='line_chart_json_asset'),
    path('chartJSON_Debit', line_chart_json_debit, name='line_chart_json_debit'),
    path('chartJSON_Credit', line_chart_json_credit, name='line_chart_json_credit'),
    path('chartJSON_Expense', line_chart_json_expense, name='line_chart_json_expense'),
    path('chartJSON_Products_Sold', line_chart_json_products_sold, name='line_chart_json_products_sold'),
    path('chartJSON_Account', line_chart_json_account, name='line_chart_json_account'),
    path('chartJSON_Net_Profit', line_chart_json_net_profit, name='line_chart_json_net_profit'),
    #Accounting
    path('daily_accounting',daily_accounting,name='daily_accounting'),
    #store
    
    
    path('remove_to_store',remove_to_store,name='remove_to_store'),
    path('remove_to_checkout',remove_to_checkout,name='remove_to_checkout'),
    path('remove_to_homepage',remove_to_homepage,name='remove_to_homepage'),
    path('remove_to_orders',remove_to_orders,name='remove_to_orders'),
    path('become_vendor',become_vendor,name='become_vendor'),
    #path('become_vendor/',become_vendor,name='become_vendor'),
    path('become_vendor1',become_vendor1,name='become_vendor1'),
    path('login',Login, name='login'),
    path('Dashboard',Dashboard, name='Dashboard'),
    path('Payment',payment, name='payment'),
    path('view_admin',view_admin, name='view_admin'),
    path('Vdeleteproduct',Vdeleteproduct, name='Vdeleteproduct'),
    path('stopvending',stopvending, name='stopvending'),
    path('vendor_add_product',vendor_add_product, name='vendor_add_product'),
    path('accounts/login',Login),
    path('blog', PostListView.as_view(), name='blog'),
    path('vdetail/<int:id>',vdetail, name='vdetail'),
    path('user/<str:username>', UserPostListView.as_view(), name='user_posts'),
    path('post/<int:pk>', PostDetailView.as_view(), name='post_detail'),
    path('post/new', PostCreateView.as_view(), name='post_create'),
    path('post/<int:pk>/update', PostUpdateView.as_view(), name='post_update'),
    path('post/<int:pk>/delete', PostDeleteView.as_view(), name='post_delete'),
    path("about_us", views.about_us, name="about_us"),
    path('post/<int:pk>/comment', add_comment, name='add_comment'),
    path('add_remove_cart', Index.as_view(), name='add_remove_cart'),
    path('store', store , name='store'),
    path('', homepage , name='home'),
    
    path('search', search, name='search'),
    path('signup', signup, name='signup'),
    path('checkout1', checkout1, name='checkout1'),
    path('accounts/login',Login, name='login'),
    path('login',Login, name='login'),
    path('Contact1',Contact1, name='Contact1'),
    path('contact',Contact, name='Contact'),
    path('Contact_Us1',Contact_Us1, name='Contact_Us1'),
    path('Contact_Us',Contact_Us, name='Contact_Us'),
    path('Vendor_update_get',Vendor_update_get, name='Vendor_update_get'),
    path('Vendor_update',Vendor_update, name='Vendor_update'),
    path('<int:id>/product_update',Product_update, name='Product_update'),
    path('Payment_update',Payment_update, name='Payment_update'),
    path('productboard',productboard, name='productboard'),
    path('Brand_add', Brand_add , name='Brand_add'),
    path('Category_add', Category_add , name='Category_add'),
    path('<int:id>/Brand_update', Brand_update , name='Brand_update'),
    path('<int:id>/Category_update', Category_update , name='Category_update'),
    path('<int:id>/Product_delete', Product_delete , name='Product_delete'),
    path('<int:id>/Category_delete', Category_delete , name='Category_delete'),
    path('<int:id>/Brand_delete', Brand_delete , name='Brand_delete'),
    path('logout', Logout , name='logout'),
    path('<int:id>/details', details , name='details'),
    #cart
    path('cart',lart, name='lart'),
    path('clearcart',clearcart,name='clearcart'),
    path('remove_to_cart', remove_to_cart , name='remove_to_cart'),


    
    path('check-out', checkout , name='checkout'),
    #path('orders', orders, name='orders'),
    path('<int:id>/delete', delete , name='delete'),
    path('reset_password',auth_views.PasswordResetView.as_view(template_name='Change-password.html',
            success_url = '/reset_password_sent'),name="reset_password"),
    path('reset_password_sent',auth_views.PasswordResetDoneView.as_view(template_name='Change-password-sent.html'),name="password_reset_done"),
    path('reset/<uidb64>/<token>',auth_views.PasswordResetConfirmView.as_view(template_name='Change-password-new.html'),name="password_reset_confirm"),
    path('reset_password_complete',auth_views.PasswordResetCompleteView.as_view(template_name='Change-password-finish.html'),name="password_reset_complete"),

    #ARCRID SPECIFIC
    path("about_us", views.about_us, name="about_us"),
    path('privacy-policy', views.privacy_policy, name='privacy_policy'),
    path('terms-and-conditions', views.terms_and_conditions, name='terms_and_conditions'),
    path('delivery-information', views.delivery_information, name='delivery_information'),
    path('return-policy', views.return_policy, name='return_policy'),

    #likes
    path('liked_products', product_list, name='product_list'),
    path('toggle_like/<int:product_id>/', toggle_like, name='toggle_like'),
    path('automated', PaymentView.as_view(), name='payment'),
    path('download/', download_app, name='download_app'),
    path(
        "pay/<str:ordering_code>/",
        PaymentView_button.as_view(),
        name="pesapal_pay",
    ),
    path(
        "cancel/<str:ordering_code>/",
        cancel_order,
        name="cancel_order",
    ),
    path('billing_terms',billing_terms,name='billing_terms'),

    path('pesapal/callback/', pesapal_callback, name='pesapal_callback'),


    path('orders/', OrderHistoryView.as_view(), name='order_history'),
    
    # Optionally add an order detail view:
    #path('orders/<str:ordering_code>/', views.OrderDetailView.as_view(), name='order_detail'),
    path('confirm_deletion', confirm_account_action, name='confirm_account_action'),
    path('account/deactivated', deactivate_account, name='account_deactivated'),
    path('account/deleted', delete_account, name='account_deleted'),
]



'''
    path('pesapal/payment/<str:ordering_code>/', views.get_pesapal_payment_iframe, name='pesapal_payment'),
    
    path(
        "payments/pesapal/ipn/",
        PesapalIPNView.as_view(),
        name="pesapal_callback"
    ),
    ''',