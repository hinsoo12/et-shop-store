from django.contrib import admin
from .models import *

# admin.site.register(Cart)
# admin.site.register(CartItem)

class CartItemInline(admin.TabularInline):
    model = CartItem
    raw_id_fields = ['product']
    extra = 0

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id']
    inlines = [CartItemInline]
