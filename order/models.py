from django.db import models
from django.utils.safestring import mark_safe
from django.db.models.signals import post_save
from account.models import User
from address.models import Address
from coupon.models import Coupon ,CouponUser
from django.conf import settings
 
ORDER_STATUS =(
    ('Order Received','Order Received'),
    ('Order Processing','Order Processing'),
    ('On the way','On the way'),
    ('Order Completed','Order Completed'),
    ('Order Canceled','Order Canceled'),
)

METHOD =(
    ("Cash On Delivery","Cash On Delivery"),
    ("Telebirr",'Telebirr'),
    ("CBE",'CBE'),
    ("Awash Bank",'Awash Bank'),
    ("CBO",'CBO'),
    ("Chapa",'Chapa'),
)

 
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    #user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, null=True)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True)
    instruction = models.TextField(max_length=500, blank=True , null=True)
    contact_number = models.CharField(max_length=10, null=True , blank=True)
    total = models.BigIntegerField(null=True, blank=True)
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True , blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True) 
    delivery_charge = models.BigIntegerField()
    payment_method=models.CharField(max_length=20,choices=METHOD,default="Cash On Delivery")
    payment_completed=models.BooleanField(default=False)
 
    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return 'Order {} {}'.format(self.user, self.id)

    def sub_total(self):
        return sum(item.total for item in self.order_items.all())
 


ORDER_ITEM_STATUS_CHOICES= (
    ('Received','Received'),
    ('Processing','Processing'),
    ('In_Delivery','In Delivery'),
    ('Completed', 'Completed'),
    ('Cancelled', 'Cancelled'),
    ('Cancelled_Delivery', 'Cancelled Delivery'),
    ('Returned', 'Returned'),
)

 
class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='order_items', on_delete=models.CASCADE,)
    product = models.ForeignKey("product.Product", related_name='order_products', on_delete=models.CASCADE,)
    price = models.BigIntegerField()
    quantity = models.PositiveIntegerField(default=1)
    color = models.CharField(max_length=50, null=True , blank=True)
    size = models.CharField(max_length=50, null=True , blank=True)
    item_status = models.CharField(choices= ORDER_ITEM_STATUS_CHOICES, default="Received" ,max_length=50)
    created = models.DateTimeField(auto_now_add=True)
    total = models.BigIntegerField()


    def __str__(self):
        return '{}'.format(self.id)


    def coupon_used(self):
        return self.order.coupon


    def status(self):
        if self.item_status == "Received":
            return mark_safe('<span class="badge border bg-light-primary text-dark-primary font-size-xs px-2 mb-3 mb-md-0"> Order Received </span>')
        elif self.item_status == "Processing":
            return mark_safe('<span class="badge border bg-light-warning text-dark-warning font-size-xs px-2 mb-3 mb-md-0">Processing</span>')
        elif self.item_status == "In_Delivery":
            return mark_safe('<span class="badge border bg-primary font-size-xs px-2 mb-3 mb-md-0">In Delivery</span>')
        elif self.item_status == "Completed":
            return mark_safe('<span class="badge border bg-light-success text-dark-success font-size-xs px-2 mb-3 mb-md-0">Completed</span>')
        elif self.item_status == "Cancelled":
            return mark_safe('<span class="badge border bg-light-secondary text-dark-secondary font-size-xs px-2 mb-3 mb-md-0">Cancelled</span>')
        elif self.item_status == "Cancelled_Delivery":
            return mark_safe('<span class="badge border bg-light-secondary text-dark-secondary font-size-xs px-2 mb-3 mb-md-0">Cancelled Delivery</span>')
        elif self.item_status == "Returned":
            return mark_safe('<span class="badge border bg-light-danger text-dark-danger font-size-xs px-2 mb-3 mb-md-0">Returned</span>')


def order_post_save_receiver(sender, instance, created, *args, **kwargs):
    if created:
        try:
            if instance.coupon:
                CouponUser.objects.create(user=instance.user,coupon=instance.coupon)
        except:
            pass
post_save.connect(order_post_save_receiver, sender=Order)
        

class ReturnOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    order_item = models.ForeignKey(OrderItem, on_delete=models.SET_NULL, null =True)
    reason = models.CharField(max_length=500, null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.reason
