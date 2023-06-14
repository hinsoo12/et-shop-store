from django.urls import path

from .views import (
    SignUpView,
    CustomerInfo,
    login_page ,
    change_password ,
    user_logout ,
    user_update,
)

urlpatterns = [
    path('signup/',SignUpView.as_view(),name='signup'),
    path('login/',login_page,name='user_login'),
    path('profile/',CustomerInfo.as_view() ,name='customerinfo'),
    path('change_information/', user_update, name='user_update'),
    path('customer/profile/change_password',change_password,name='change_password'),    
    path('logout/', user_logout, name='user_logout'), 

    #path('customer/verify/',customer_verify,name='verify-account'),
    #path('resend/',resend,name='resend'),
    #forgot passoword
    #path('reset-password/',custom_password_reset,name='custom_password_reset'),
    #path('reset-password/verify/',reset_password_verify,name='reset_password_verify'),
]
 
