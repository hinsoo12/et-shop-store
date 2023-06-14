from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.urls import path, include


urlpatterns = [
    url('^', include('django.contrib.auth.urls')),
]