from django.shortcuts import render, HttpResponseRedirect,redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import ListView , UpdateView
from .models import Address
from .forms import AddressForm
from cart.models import Cart
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

class AddressView(LoginRequiredMixin,ListView):
    model = Address
    template_name = "address.html"
    login_url = '/customer/login/' 

    def get_context_data(self, **kwargs):
        context = super(AddressView, self).get_context_data(**kwargs)
        address_list = Address.objects.filter(user=self.request.user).order_by('-created')[0:10]
        address_form = AddressForm()
        context = {
            'address_list': address_list,
            'address_form':address_form,
        }
        return context 

@login_required(login_url='/login/')
def add_address(request):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            data = Address()
            data.building =  form.cleaned_data['building']
            data.area =  form.cleaned_data['area']
            data.city =  form.cleaned_data['city']
            data.district =  form.cleaned_data['district']
            data.province =  form.cleaned_data['province']
            data.user = request.user
            data.save()
            messages.success(request, 'New address has been successfully added!')
            return HttpResponseRedirect(url)
        else:
             form = AddressForm()
    return HttpResponseRedirect(url)


@login_required(login_url='/login/')
def set_default_address(request,id):
    url = request.META.get('HTTP_REFERER')
    Address.objects.filter(user=request.user, default=True).update(default=False)
    Address.objects.filter(user=request.user, id=id).update(default=True)

    cart_obj = Cart.objects.filter(user=request.user)
    if cart_obj.count() == 1:
        cart_obj.first().update_total()

    messages.success(request, 'Your default delivery address has been successfully changed !')
    return HttpResponseRedirect(url)



@login_required(login_url='/login/')
def delete_address(request, id):
    url = request.META.get('HTTP_REFERER')
    try:
        obj = Address.objects.get(user=request.user,id=id, default=False)
        obj.delete()
        messages.success(request, 'Your address has been deleted !')
    except:
        obj = Address.objects.get(user=request.user,id=id, default=True)
        messages.warning(request, 'Cannot delete a default address. Change your default address and try deleting  again.')
    return HttpResponseRedirect(url)


class CustomerAddressUpdate(LoginRequiredMixin,UpdateView):
    form_class = AddressForm
    model = Address
    template_name = "customer_update_address.html" 
    success_url = reverse_lazy('address') 
    slug_field = 'id'
    login_url = '/customer/login/'

    def form_valid(self, form):
        super(CustomerAddressUpdate, self).form_valid(form)
        messages.success(self.request, 'Your address is successfully updated!')
        return redirect(self.success_url)

