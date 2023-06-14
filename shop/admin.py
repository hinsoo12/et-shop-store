from django.contrib import admin
from .models import Pages ,Sliders, Sale, SalesItem

#admin.site.register(Pages) 

@admin.register(Sliders)
class SildersOrderAdmin(admin.ModelAdmin):
    list_display = ['is_active']


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ['cashier','total','date']
    search_fields = ['cashier']
    list_per_page = 50
    list_filter = ['date']
    ordering = ['-date']

@admin.register(SalesItem)
class SalesItemAdmin(admin.ModelAdmin):
    list_display = ['sale','product','quantity','subtotal']
    search_fields = ['sale','product']
    list_per_page = 50
    list_filter = ['date']
    ordering = ['-date']