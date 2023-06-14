from django.db import models
from account.models import User
from order.models import OrderItem
from django.core.validators import MaxValueValidator, MinValueValidator

# parent__isnull=True ==> This reperesents all the reviews from customers only.
  
class Review(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    order_item = models.ForeignKey(OrderItem, on_delete=models.CASCADE , null=True ,related_name="item_review")
    content = models.TextField(blank=True)
    stars = models.IntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)] , null=True , blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='reply')
    created = models.DateTimeField(auto_now_add=True)

    class Meta: 
        ordering = ('-created',)

    def __str__(self):
        return str(self.order_item.product)+"---"+str(self.user) 

    

