from django.db import models
from product.models import Product , Variation
from address.models import Address
from account.models import User
from coupon.models import Coupon
from django.utils.safestring import mark_safe
from django.db.models.signals import pre_save, m2m_changed ,post_save ,pre_delete ,post_delete
from django.core.exceptions import ObjectDoesNotExist

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True , related_name="cart_user")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)  
    total = models.BigIntegerField(null=True, blank=True)
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True , blank=True , related_name='carts')

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return 'Cart of {}'.format(self.user.first_name)

    def update_total(self):
        self.total = sum(item.total for item in self.items.all()) + self.delivery_charge() - self.get_discount()
        self.save()
        return self.total

    @property
    def get_coupon(self):
        if self.coupon:
            try:
                coupon = Coupon.objects.get(id=self.coupon_id)
                if coupon.purchase > self.verify_amount():
                    self.coupon = None
                else:
                    return coupon
            except Coupon.DoesNotExist:
                pass
        return None

    def verify_amount(self):
        if self.coupon:
            return sum(item.total for item in self.items.all())

    def sub_total(self):
        return sum(item.total for item in self.items.all())

    def delivery_charge(self):
        return sum(item.delivery_price() for item in self.items.all())

    def get_discount(self):
        if self.get_coupon:
            return self.coupon.value
        return float(0)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', null=True, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE ,related_name="cart_product")

    color = models.CharField(max_length=50,null=True , blank=True)
    size = models.CharField(max_length=50,null=True , blank=True)

    price = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField(default=1)
    total = models.BigIntegerField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return '{}'.format(self.product.title)

    def delivery_price(self):
        try:
            current_address = Address.objects.get(user=self.cart.user , default=True)
            if current_address.district == "Addis Ababa" or current_address.district == "Sheger City" :
                return 150

            elif current_address.district == "Adama" or current_address.district == "Bishoftu" or current_address.district == "Mojo" :
                return 250
                
            else:
                return 500
        except:
            return 0
 

def pre_save_cart_item_receiver(sender, instance, *args, **kwargs):
    instance.total = int(instance.price) * int(instance.quantity)
pre_save.connect(pre_save_cart_item_receiver, sender=CartItem)


def cart_item_pre_delete_receiver(sender, instance, *args, **kwargs):
    try:
        cart = instance.cart.update_total()
    except ObjectDoesNotExist:
        pass
post_delete.connect(cart_item_pre_delete_receiver, sender=CartItem)


def cart_item_total_post_save_receiver(sender, instance, created, *args, **kwargs):
    if not created: 
        instance.cart.update_total()
post_save.connect(cart_item_total_post_save_receiver, sender=CartItem)


















        







