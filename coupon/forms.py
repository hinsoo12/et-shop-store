from django.forms import ModelForm
from django.contrib import messages
from django.contrib.auth.models import User
from django import forms
from .models import Coupon , CouponUser
from cart.models import Cart , CartItem
from crispy_forms.helper import FormHelper
from django.forms import TextInput
from functools import partial



class CouponApplyForm(forms.Form):
    code = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control form-control-sm",'placeholder':"Apply Coupon Code"}))

    def __init__(self, *args, **kwargs):
        self.user = None
        if 'user' in kwargs:
            self.user = kwargs['user']
            del kwargs['user']
        super(CouponApplyForm, self).__init__(*args, **kwargs)
        self.fields['code'].label = False
 
    def clean_code(self):
        code = self.cleaned_data['code']
        try:
            coupon = Coupon.objects.get(code=code)            
        except Coupon.DoesNotExist:
            raise forms.ValidationError("This code is not valid.")
        self.coupon = coupon

        if coupon.expired():
            raise forms.ValidationError("This code is expired.")

        if coupon.is_redeemed:
            raise forms.ValidationError("This code has already been used-up.")

        try:
            user_coupon = coupon.users.get(user=self.user)
            raise forms.ValidationError("You have already used this codes.")
        except CouponUser.DoesNotExist:
            pass

        cart = Cart.objects.get(user=self.user)
        cartitems = sum(item.total for item in cart.items.all())
        if cartitems < coupon.purchase:
            raise forms.ValidationError("Purchase amount not enough.")


        return code
 