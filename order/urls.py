from django.urls import path

from .views import (
    order_processing, 
    CustomerOrders, 
    ajax_return_product,
    product_return, 
    TeleBirrRequestView, 
    CBERequestView,
    AwashBirrRequestView,
    CBOEBirrRequestView,

)

urlpatterns = [
    # cash on delivery 
    path('cash-on-delivery-save_order/', order_processing, name="save_order"),
    
    path('customer/orders/', CustomerOrders.as_view(), name="customer_orders"),

    path('ajax_return_order/', ajax_return_product, name="return_order"),
    path('product_return/<int:id>', product_return, name="product_return"),
    
    # payment requests
    path('telebirr-request/',TeleBirrRequestView.as_view(),name='telebirr_request'),
    path("cbe-request/", CBERequestView.as_view(), name="cbe_request"),
     path('awash-request/',TeleBirrRequestView.as_view(),name='awash_birr_request'),
    path("cbo-request/", CBERequestView.as_view(), name="cbo_ebirr_request"),
    
]   
