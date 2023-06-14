from django.urls import path
from wishlist import views

urlpatterns = [
    path('wishlist_add/<int:id>/', views.wishlist_add, name='wishlist_add'),
    path('wishlist_remove/<int:id>/', views.wishlist_remove, name='wishlist_remove'),
    path('customer/saved_products/', views.MyWishlist.as_view(), name="saved_products"),
]      