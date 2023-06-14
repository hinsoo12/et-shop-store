from django.db import models
from django.urls import reverse
from ckeditor.fields import RichTextField
from account.models import User
from product.models import Product

class Sliders(models.Model):
    image = models.ImageField(upload_to='sliders/')
    url = models.CharField(max_length=500 , blank=True)
    is_active = models.BooleanField(default=True)
    class Meta:
        verbose_name = ("Slider")
        verbose_name_plural = ("Sliders")
      
class Pages(models.Model):
    name = models.CharField(max_length=100)
    content = RichTextField(blank=True)
    slug = models.SlugField(unique=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = ("Page")
        verbose_name_plural = ("Pages")

    def get_absolute_url(self):
        return reverse("pages", kwargs={"slug":self.slug})


class Sale(models.Model):
    # A model for a sale made by a cashier
    cashier = models.ForeignKey(User, on_delete=models.CASCADE) # The cashier who made the sale
    products = models.ManyToManyField(Product) # The products in the sale
    total = models.DecimalField(max_digits=10, decimal_places=2) # The total amount of the sale
    date = models.DateTimeField(auto_now_add=True) # The date and time of the sale
    
    class Meta:
        verbose_name = ("Sale")
        verbose_name_plural = ("Sales")

    def __str__(self):
        return f'Sale #{self.id} by {self.cashier.username}'

class SalesItem(models.Model):
    # A model for an item in a sale
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE) # The sale that contains the item
    product = models.ForeignKey(Product, on_delete=models.CASCADE) # The product that is the item
    quantity = models.PositiveIntegerField() # The quantity of the product in the item
    subtotal = models.DecimalField(max_digits=10, decimal_places=2) # The subtotal amount of the item
    date = models.DateTimeField(auto_now_add=True) # The date and time of the sale

    class Meta:
        verbose_name = ("SalesItem")
        verbose_name_plural = ("SalesItems")

    def __str__(self):
        return f'{self.quantity} x {self.product.name}'

