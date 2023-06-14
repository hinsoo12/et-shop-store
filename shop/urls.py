from django.urls import path
from .views import Home ,PageDetail, search_product
   
urlpatterns = [
    path('',Home.as_view() , name='home'),
    path('page/<slug>/',PageDetail.as_view() , name='pages'),
    path('search-product/',search_product , name='search-product'),
]


