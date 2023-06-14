from django.db import models
from account.models import User
from django.utils.translation import ugettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone
import random
from datetime import datetime, timedelta

VALIDITY= (
    ('1','1 day'),
    ('3', '3 days'),
    ('7', '7 days'),
    ('15', '15 days'),
    ('30', '30 days'),
)
 
class Coupon(models.Model):
    coupon_name = models.CharField(max_length=30, unique=True)
    code = models.CharField(max_length=30, unique=True)
    value = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(5000)])
    purchase =  models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(100000)], help_text='must equal to product prize')
    validity = models.CharField(choices=VALIDITY,max_length=50 ,default="30")
    quantity = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.code
 
    def time_remain(self):
        return datetime.now() + timedelta(days=int(self.validity))

    def expired(self):
        valid = timezone.now() + timedelta(days=int(self.validity))
        return valid < timezone.now()

    def used_count(self):
        return self.users.count()

    def coupon_left(self):
        return self.quantity - self.used_count()

    def coupon_left_percentage(self):
        return round(self.used_count()/self.quantity *100)
    
    @property
    def is_redeemed(self):
        return self.users.count() >= self.quantity and self.quantity != 0


class CouponUser(models.Model):
    coupon = models.ForeignKey(Coupon, related_name='users', on_delete= models.CASCADE)
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    redeemed_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return str(self.user)
