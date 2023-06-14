from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect ,reverse
from django.conf import settings
from django.utils import timezone
from product.models import Product
from .models import Cart, CartItem
from address.models import Address
from coupon.models import Coupon ,CouponUser
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, TemplateView
from coupon.forms import CouponApplyForm
from django.views.generic.edit import FormMixin


@login_required(login_url='/login/')
def cart_add_q(request, id, product_qty=None):
    obj, created = Cart.objects.update_or_create(user=request.user)
    product = get_object_or_404(Product, id=id)
    price = product.selling_price
    item, itemCreated = CartItem.objects.update_or_create(cart=obj, product=product , price=price)
    item.color = request.GET.get('color')
    item.size = request.GET.get('size')
    item.quantity = request.GET.get('quantity')
    if  request.GET.get('quantity') == "0":
        item.delete()
    else:
        obj.items.add(item)
        item.save()
        obj.save()
    return redirect('cart') 
    
    
@login_required(login_url='/login/')
def add_quantity(request, id, product_qty=None):
    url = request.META.get('HTTP_REFERER')
    cart = Cart.objects.get(user=request.user)
    product = get_object_or_404(Product, id=id)
    item = CartItem.objects.get(cart=cart, product=product)
    item.quantity = item.quantity+1
    item.save()
    return HttpResponseRedirect(url)

def dec_quantity(request, id, product_qty=None):
    url = request.META.get('HTTP_REFERER')
    try:
        cart = get_object_or_404(Cart ,user=request.user)
        product = get_object_or_404(Product, id=id)
        item = CartItem.objects.get(cart=cart, product=product)
        item.quantity = item.quantity-1
        if item.quantity <= 0:
            item.delete()
        else:
            item.save()
        return HttpResponseRedirect(url)
    except:
        return HttpResponseRedirect(url)

@login_required(login_url='/login/')
def cart_remove(request, product_id):
    obj, created = Cart.objects.update_or_create(user=request.user)
    product = get_object_or_404(Product, id=product_id)
    cartItems = CartItem.objects.filter(cart=obj, product=product)
    cartItems.delete()
    return redirect('cart:cart_detail')
 

@login_required(login_url='/login/')
def cart_view(request):
    address = Address.objects.filter(user=request.user)  

    cart , created= Cart.objects.get_or_create(user=request.user)
    coupon_apply_form = CouponApplyForm(request.POST or None , user=request.user)

    context = {
            "coupon_apply_form": coupon_apply_form,
            "address": address,
            "cart": cart,
            }
    if coupon_apply_form.is_valid():
        code = coupon_apply_form.cleaned_data.get('code')
        coupon = Coupon.objects.get(code=code)
        cart = Cart.objects.filter(user=request.user)
        cart.update(coupon=coupon) 
        if cart.count() == 1:
            cart.first().update_total()
        return redirect('cart')

    return render(request, 'cart.html', context) 


class OrderSuccess(TemplateView):
    template_name = "order_success.html"
 

    
