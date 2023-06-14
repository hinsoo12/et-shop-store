from django.urls import path
from .views import ProductDetail , CategoryView
   
urlpatterns = [
    path('product/<slug>',ProductDetail.as_view() , name='product_detail'),
    path('category/',CategoryView.as_view() , name='category'),
]