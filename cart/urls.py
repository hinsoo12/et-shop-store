from django.urls import path
from .views import cart_add_q ,cart_remove , cart_view , OrderSuccess , add_quantity , dec_quantity

# CartView

urlpatterns = [
    # path('checkout/', CartView.as_view(), name="cart"),
    path('checkout/', cart_view, name="cart"),

    path('order_success/', OrderSuccess.as_view(), name="order_success"),
    
    path('add_to_cart/<int:id>/', cart_add_q, name="add_to_cart"),

    path('add_quantity/<int:id>/', add_quantity, name="add_quantity"),
    path('dec_quantity/<int:id>/', dec_quantity, name="dec_quantity"),
]   

