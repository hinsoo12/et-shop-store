from django.contrib import admin
from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['content','reviewed_by','created']
    search_fields = ['content','reviewed_by']
    list_per_page = 100
    list_filter = ['created']
    ordering = ['-created']

    def reviewed_by(self, obj):
      return obj.user.get_full_name()
       
