from django.db import models
from account.models import User
from django.db.models.signals import pre_save,post_save
from django.dispatch import receiver


DISTRICTS= (
    ('Addis Ababa','Addis Ababa'),
    ('Sheger City','Sheger City'),
    ('Adama','Adama'),
    ('Bishoftu','Bishoftu'),
    ('Mojo','Mojo'),
    ('Hawassa','Hawassa'),
    ('Arba-Minch','Arba-Minch'),
    ('Woliata-Soddo','Woliata-Soddo'),
    ('Dire Dewa','Dire Dawa'),
    ('Harar','Harar'),
    ('Jimma','Jimma'),
    ('Bahirdar','Bahirdar'),
    ('Gondar','Gondar'),
    ('Mekele','Mekele'),
    ('Bahirdar','Bahirdar'),

)

PROVINCE = (
    ('one','Province No. 1'),
    ('two', 'Province No. 2'),
    ('three','Province No. 3'),
    ('four', 'Province No. 4'),
)
  
class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    building = models.CharField(max_length=120,blank=True,null=True)
    area = models.CharField(verbose_name="Area",max_length=100, null=True, blank=True)
    city = models.CharField(verbose_name="City/Town",max_length=50)
    district = models.CharField(choices=DISTRICTS,verbose_name="District",max_length=100, default="Kathmandu")
    province = models.CharField(choices=PROVINCE,verbose_name="Province",max_length=100, default="three")
    default = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta: 
        verbose_name = ("Address")
        verbose_name_plural = ("Address")
        ordering = ('-created',)
        
    def __str__(self):
        return str(self.user)

    def __str__(self):
        return 'Address of {} with id {}'.format(self.user, self.id)

    def current_address(self):
        return Address.objects.get(user=self.request.user, default=True)
