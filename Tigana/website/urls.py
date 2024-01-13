
from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


from . import views

app_name = 'website'
urlpatterns = [
    # ex: /website/shop
    path('shop', views.shop.as_view(), name='shop'),
    # ex: /website/shop/id
    path('shop/<int:id>/', views.shop_detail.as_view(), name='shop_detail'),
    # ex: /inquiry/received
    path('inquiry/received',views.inquiry_received.as_view(), name='received'),
    # ex: /website/contact
    path('contact',views.contact.as_view(), name='contact'),
    # ex: /website/cart
    path('cart',views.cart.as_view(), name='cart'),
    # ex: /website/cart
    path('cart/<int:id>',views.cart.as_view(), name='cart'),
    # ex: /website/orderconfirmation
    path('orderconfirmation',views.cart_confirmation.as_view(), name='orderconfirmation'),
    # ex: /website/ordercomplete
    path('ordercomplete',views.cart_order_done.as_view(), name='ordercomplete'),
]

urlpatterns += staticfiles_urlpatterns()
