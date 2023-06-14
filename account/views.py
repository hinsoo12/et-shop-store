from django.contrib.auth import login,authenticate ,update_session_auth_hash , logout
from django.utils.decorators import method_decorator
from django.shortcuts import redirect ,render, HttpResponseRedirect
from account.models import User
from account.forms import SignUpForm, LoginForm, PasswordChangeCustomForm , UserUpdateForm
from django.views.generic import (View,ListView, CreateView, UpdateView, TemplateView)
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin


class SignUpView(CreateView):
    model = User
    form_class = SignUpForm
    template_name= 'customer_signup.html'
    success_url = reverse_lazy('user_login')
    success_message = "Your account was created successfully."

def login_page(request):
    form = LoginForm(request.POST or None)
    valuenext= request.POST.get('next')
    if form.is_valid():
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            try:
             # Log in the user
                login(request, user)
                return redirect('home')
                #return render(request,'home.html')
            except:
                messages.warning(request, "Invalid credentials. Try Again")
                return redirect('customer-login')
        
    #messages.info(request, "Invalid credentials. Try Again.")
    return render(request, 'customer_login.html',  {'form': form })


class CustomerInfo(ListView):
    model = User
    template_name = "customerinfo.html"

@login_required(login_url='/login/')
def user_update(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your personal information has been updated!')
            return redirect('customerinfo')
    else: 
        form = UserUpdateForm(instance=request.user)
        context = {
            'form': form,
        } 
        return render(request, 'user_update.html', context)


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeCustomForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('customerinfo')
    else:
        form = PasswordChangeCustomForm(request.user)
    return render(request, 'change_password.html', {'form': form })

def user_logout(request):
    logout(request)
    return redirect('user_login')

 