from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from requests.models import codes
from account.models import User
from django.contrib.auth.models import Group
import django.apps
from django.contrib.admin.models import LogEntry, DELETION
from django.urls import reverse
from django.utils.html import escape
from django.utils.safestring import mark_safe
from django import forms
from django.forms import ModelForm 

#admin.site.unregister(Group)

@admin.register(User)
class AccountAdmin(UserAdmin):
    date_hierarchy = 'date_joined'
    list_display = ('full_name','email','is_staff', 'is_active',)
    ordering = ('-date_joined',)
        
    search_fields = ('email',)

    def full_name(self, obj):
	    return obj.get_full_name()
 

