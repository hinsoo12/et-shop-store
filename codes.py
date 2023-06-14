def dispatch(self, request, *args, **kwargs):
    b_address, s_address = self.get_address()
    if not (b_address.exists() and s_address.exists()):
        messages.success(self.request, 'Please add an address before continuing')
        return redirect('add_address')
    return super(AddressFormView, self).dispatch(request, *args, **kwargs)

def ajax_product_by_list(request):
    cat_id = request.GET.get('id', None)
    slug = request.GET.get('slug', None)
    category = Category.objects.get(id=cat_id)
    seller = Seller.objects.get(slug=slug)
    products = Product.objects.filter(category=category,seller=seller)
    return render(request, 'by_category.html', {'products': products , "category":category}) 
   


def create_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = Post.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" %(slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug



used_count = models.IntegerField(default=0, editable=False)
def update_usage(self, inc=1, force_save=False):
    self.used_count = F('used_count') + inc
    if force_save:
        self.save(update_fields=['used_count'])