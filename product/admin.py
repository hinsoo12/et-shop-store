from django.contrib import admin
from .models import Product, Category


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title','brand','category','sub_category','selling_price','offering_price','is_active']
    search_fields = ['title','category','selling_price','is_active']
    list_per_page = 50
    list_filter = ['published']
    ordering = ['-updated']

       
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name','parent']
    search_fields = ['name','parent']
    list_per_page = 50
    list_filter = ['name']
    #ordering = ['-name']

   
       
