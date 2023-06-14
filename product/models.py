from django.db import models
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.db.models import Count, Sum, Avg
from helper import unique_slug_generator,file_size
from django.db.models.signals import pre_save
from django.template.defaultfilters import slugify
from django.core.exceptions import ValidationError
from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import SearchVector, SearchVectorField 
from urllib.parse import urlparse ,parse_qs
from mptt.models import MPTTModel, TreeForeignKey
from ckeditor.fields import RichTextField
from account.models import User 
from review.models import Review


class ActiveProductManager(models.Manager):
    def get_queryset(self):
        return super(ActiveProductManager, self).get_queryset().filter(is_active=True)


class Category(MPTTModel):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children',on_delete=models.SET_NULL)
    image = models.ImageField(blank=True,upload_to='category/',validators=[file_size])

    
    class Meta:
        verbose_name = ("Category")
        verbose_name_plural = ("Categories")
        ordering = ("-name",)

    def __str__(self):
        return self.name

    class MPTTMeta:
        order_insertion_by = ['id']

    def get_absolute_url(self):
        return reverse("category", kwargs={"slug":self.slug})

 
class Product(models.Model):
 
    # Basic Information
    title = models.CharField(max_length=500)
    brand = models.CharField(max_length=120, blank= True)

    category = models.ForeignKey('Category',null=True,on_delete=models.SET_NULL,related_name="product_catgeory")
    sub_category = models.ForeignKey('Category',null=True,on_delete=models.SET_NULL,related_name="product_subcatgeory")

    # pricing
    selling_price = models.BigIntegerField()
    offering_price = models.BigIntegerField()

    #Images
    image = models.ImageField(upload_to='product/' ,validators=[file_size])
    img_second = models.ImageField(blank=True,upload_to='product/',validators=[file_size])
    img_third = models.ImageField(blank=True,upload_to='product/',validators=[file_size])
    img_forth = models.ImageField(blank=True,upload_to='product/',validators=[file_size])
    img_fifth = models.ImageField(blank=True,upload_to='product/',validators=[file_size])
    video = models.URLField(blank=True , null=True)

    #Description
    description = RichTextField(blank=True)

    slug = models.SlugField(null=True, unique=True,max_length=500)
    published = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)  
    is_active = models.BooleanField(default=True)
    objects = models.Manager()
    active = ActiveProductManager()
   
    
    def __str__(self):
        return self.title

    class Meta:
        verbose_name = ("Product")
        verbose_name_plural = ("Products")
        ordering = ("-published",)

       

    def get_absolute_url(self):
        return reverse("product_detail", kwargs={"slug":self.slug})

    def status(self):
        if self.is_active:
            return mark_safe('<span class="badge-dot bg-success mr-1 d-inline-block align-middle"></span>Live')
        else:
            return mark_safe('<span class="badge-dot bg-warning mr-1 d-inline-block align-middle"></span>In Review')


    def saved_price(self):
        try:
            return self.offering_price-self.selling_price
        except:
            pass

 
    def discount_percentage(self):
        if self.saved_price:
            return int((self.saved_price()/self.offering_price) * 100)

    def clean(self):
        if self.selling_price > self.offering_price:
            raise ValidationError(
                {'price': "Your selling price must be less than maximum retail price."})
                   

    def average_review(self):
        reviews = Review.objects.select_related("order_item__product" ,'parent').filter(order_item__product=self ,parent__isnull=True).aggregate(average=Avg('stars'))
        avg = 0
        if reviews['average'] is not None:
            avg = float(reviews['average'])
            return avg
        else:
            return avg

    def total_review(self):
        reviews = Review.objects.select_related("order_item__product" ,'parent').filter(
            order_item__product=self,parent__isnull=True).aggregate(count=Count('id'))
        cnt = 0
        if reviews['count'] is not None:
            cnt = (reviews['count'])
            return cnt

    def get_video_id(self):
        u_pars = urlparse(self.video)
        quer_v = parse_qs(u_pars.query).get('v')
        if quer_v:
            return quer_v[0]
        pth = u_pars.path.split('/')
        if pth:
            return pth[-1] 



class VariationManager(models.Manager):
    def colors(self):
        return super(VariationManager, self).filter(variation_category='Color')

    def sizes(self):
        return super(VariationManager, self).filter(variation_category='Size')


variation_category_choice = (
    ('Color', 'Color'),
    ('Size', 'Size'),
)

class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE ,related_name= "product_variation")
    variation_category = models.CharField(max_length=100, default="Color" ,choices=variation_category_choice, blank=True)
    variation_value = models.CharField(max_length=100 ,blank=True)

    objects = VariationManager()

    def __str__(self):
        return self.variation_value


 
def product_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance=instance)
    
pre_save.connect(product_pre_save_receiver, sender=Product)  


