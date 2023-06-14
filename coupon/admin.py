from django.contrib import admin
from .models import Coupon , CouponUser

class CouponUserInline(admin.TabularInline):
    model = CouponUser
    extra = 0
 
@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ['code','discount','min_purchase','quantity','time_remain','active']
    list_display_links =  ['code']
    search_fields = ['code']
    list_per_page = 100
    list_filter = ['created_at']
    inlines = [CouponUserInline]  


    def discount(self, obj):
	    return  str(obj.value) + ' Birr'

    def min_purchase(self, obj):
	    return str(obj.purchase) + ' Birr'

    