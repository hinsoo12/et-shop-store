from django.urls import path
from .views import AddressView ,add_address ,set_default_address, delete_address , CustomerAddressUpdate

urlpatterns = [
    path('customer/address/',AddressView.as_view(),name='address'),
    path('add_address/',add_address,name='add_address'),
    path('change_address/<int:id>',set_default_address,name='change_address'),
    path('remove_address/<int:id>',delete_address,name='remove_address'),
    path("customer/address/update/<int:pk>/",CustomerAddressUpdate.as_view(), name="update_c_address"),
]
