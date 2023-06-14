from django import forms
from django.contrib.auth.forms import UserCreationForm,PasswordChangeForm ,UserChangeForm
from django.contrib.auth import login, authenticate
from django.db import transaction
from account.models import User
from address.models import Address
from django.forms import ModelForm ,Textarea, TextInput, EmailInput, PasswordInput, FileInput 
from crispy_forms.helper import FormHelper

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, label="first_name", widget=forms.TextInput(
        attrs={'class': "form-control form-control-sm",'placeholder':"First Name"}))
    last_name = forms.CharField(max_length=100, label="last_name", widget=forms.TextInput(
        attrs={'class': "form-control form-control-sm",'placeholder':"Last Name"}))
    email = forms.EmailField(max_length=200, label='email', widget=forms.EmailInput(
        attrs={'class': "form-control form-control-sm",'placeholder':"Enter your email"}))
    phone = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder':"Enter your mobile number" ,'class': "form-control form-control-sm"}))
    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs = { 'class': "form-control form-control-sm",'placeholder':"****************"})) 
    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs = { 'class': "form-control form-control-sm",'placeholder':"****************"}))

    class Meta:
        model = User
        fields = ['email', 'phone', 'first_name','last_name', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False

class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(
        attrs={'placeholder':"Email address" ,'class': "form-control"}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Password'}
    ))
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not  User.objects.filter(email__iexact=self.cleaned_data['email']):
            raise forms.ValidationError('Email address does not exists.')
        return email

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not  User.objects.filter(phone__iexact=self.cleaned_data['phone']):
            raise forms.ValidationError('Phone number does not exists.')
        return phone

    def clean_password(self):
        email = self.cleaned_data.get('email')
        phone = self.cleaned_data.get('phone')
        password = self.cleaned_data.get('password')   
 
        if email and phone and password:
            email_qs = User.objects.filter(email__iexact=self.cleaned_data['email'])
            phone_qs = User.objects.filter(phone__iexact=self.cleaned_data['phone'])
            if not email_qs.exists():
                raise forms.ValidationError("The user does not exist")
            elif not phone_qs.exists():
                raise forms.ValidationError("The user does not exist")
            else:
                #user = authenticate(phone=phone, password=password) 
                user = authenticate(email=email, password=password)   
                if not user:
                    raise forms.ValidationError("Incorrect password. Please try again!")                    
        return password

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False

class UserUpdateForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name')
        widgets = {
            'email': EmailInput(attrs={'class': 'form-control'}),
            'first_name': TextInput(attrs={'class': 'form-control'}),
            'last_name': TextInput(attrs={'class': 'form-control'}),
        }


class PasswordChangeCustomForm(PasswordChangeForm):
    def __init__(self, user, *args, **kwargs):
        super(PasswordChangeCustomForm, self).__init__(user,*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'



 
 

