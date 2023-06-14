from django.contrib import admin
from .models import Address 


class AddressAdmin(admin.ModelAdmin):
    list_display = ['user','default']
    
admin.site.register(Address, AddressAdmin)

