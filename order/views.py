from django.shortcuts import render, get_object_or_404,HttpResponseRedirect,redirect
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank , TrigramSimilarity
from django.db.models import Q
from django.contrib import messages
from django.db.models import Prefetch
from .models import Order , OrderItem, ReturnOrder
from product.models import Product
from cart.models import Cart , CartItem
from address.models import Address
from account.models import User
from django.views.generic import ListView , View
from datetime import datetime, timedelta
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse
import requests as req


@login_required(login_url='/login/')
def order_processing(request):
    if request.POST.get('address'): 
        cart = Cart.objects.get(user=request.user)
        order = Order.objects.create(user=request.user ,total=cart.total, coupon=cart.coupon , delivery_charge=cart.delivery_charge())
        order.save()
        for item in cart.items.all():
            orderItem, created = OrderItem.objects.update_or_create(
                order=order, product=item.product, price=item.price, quantity=item.quantity ,total=item.total ,color=item.color, size=item.size)
            order.order_items.add(orderItem)
        address = request.POST['address']
        order.address = Address.objects.get(id=address)
        order.instruction = request.POST['instruction']
        order.contact_number = request.POST['contact_number']
        order.payment_method = request.POST['payment_method']
        order.save()

        if request.POST['payment_method'] == "Telebirr":
            order.payment_completed = True
            order.save()
            cart.delete() 
            return redirect(reverse("telebirr_request") + "?order_id=" + str(order.id))

        elif request.POST['payment_method'] == "CBE":  
            order.payment_completed = True
            order.save()
            cart.delete()                            
            return redirect(reverse("cbe_request") + "?order_id=" + str(order.id))

        elif request.POST['payment_method'] == "Awash Bank": 
            order.payment_completed = True
            order.save()
            cart.delete()                             
            return redirect(reverse("awash_birr_request") + "?order_id=" + str(order.id))

        elif request.POST['payment_method'] == "CBO":
            order.payment_completed = True
            order.save()
            cart.delete()                              
            return redirect(reverse("cbo_ebirr_request") + "?order_id=" + str(order.id))
        else:
            order.payment_completed = True
            order.save()
            cart.delete() 
            return redirect('order_success') 
    else:
        messages.warning(request, 'Please add an address before continuing')
        return redirect('cart')


class TeleBirrRequestView(LoginRequiredMixin,View):
    def get(self,request,*args,**kwargs):
        o_id=request.GET.get('order_id')
        order= Order.objects.get(id=o_id)
        context={
             "order":order
        }
        return render(request,'telebirr-request.html',context)

class CBERequestView(LoginRequiredMixin,View):
    def get(self,request,*args,**kwargs):
        o_id=request.GET.get('order_id')
        order= Order.objects.get(id=o_id)
        context={
             "order":order
        }
        return render(request,'cbe-request.html',context)

class AwashBirrRequestView(LoginRequiredMixin,View):
    def get(self,request,*args,**kwargs):
        o_id=request.GET.get('order_id')
        order= Order.objects.get(id=o_id)
        context={
             "order":order
        }
        return render(request,'awash-request.html',context)

class CBOEBirrRequestView(LoginRequiredMixin,View):
    def get(self,request,*args,**kwargs):
        o_id=request.GET.get('order_id')
        order= Order.objects.get(id=o_id)
        context={
             "order":order
        }
        return render(request,'cbo-request.html',context)



class CustomerOrders(LoginRequiredMixin,ListView):
    model = Order
    template_name = "customer_orders.html"
    login_url = '/customer/login/' 
    paginate_by = 10

    def get_queryset(self, *args, **kwargs):
        qs = super(CustomerOrders, self).get_queryset(*args, **kwargs)
        qs = qs.prefetch_related("order_items__product").filter(user = self.request.user,payment_completed= True).order_by('-created')
        return qs 

def ajax_return_product(request):
    order_item_id = request.GET.get('id', None)
    item = OrderItem.objects.get(id=order_item_id)
    return render(request, 'return_form.html', {'item': item})


@login_required(login_url='/login/')
def product_return(request ,id):
    url = request.META.get('HTTP_REFERER')
    order_item = OrderItem.objects.get(id=id)
    reason = request.POST['reason']
    return_request = ReturnOrder.objects.update_or_create(user=request.user, reason=reason, order_item=order_item)    
    messages.success(request, 'Your product return request has been successfully sent.')
    return HttpResponseRedirect(url)


    
        