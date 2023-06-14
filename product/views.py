from django.shortcuts import render ,get_object_or_404 ,redirect
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank , TrigramSimilarity
from django.db.models import Q ,Count
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from .models import Product , Category
from datetime import datetime, timedelta
from review.models import Review 
from wishlist.models import WishlistItem
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from order.models import OrderItem
from cart.models import CartItem

def recommend_products(request, brand):
    products = Product.objects.filter(brand=brand)
    context = {'products': products}
    return render(request, 'recommend-product.html', context)

# A function that returns a list of products that belong to the same category as the given product
def get_recommended_products(product):
    category = product.sub_category
    # getting similar based on their category
    similar_products = Product.objects.filter(sub_category=category).exclude(id=product.id)

    return similar_products

# A function that returns a list of products that belong to the same category as the given product
def get_similar_products(product):
    brand = product.brand
    # getting similar based on their category
    recommended_products = Product.objects.filter(brand=brand).exclude(id=product.id)
    
    return recommended_products

class ProductDetail(DetailView):
    model = Product
    template_name = "product.html"
    paginate_by = 1


    def get_context_data(self, **kwargs): 
        slug = self.kwargs.get('slug')        
        product = Product.objects.get(slug=slug)
        # getting related product with-in the same category
        related_products = get_similar_products(product)
        # getting recommended products with the brand name
        recommended_products = get_recommended_products(product)
        
        object_list = Review.objects.prefetch_related('reply').filter(order_item__product=product, parent__isnull=True)
        context = super().get_context_data(recommended_products=recommended_products,related_products=related_products, object_list=object_list,**kwargs)
        if self.request.user.is_authenticated: 
            context["saved"] = WishlistItem.objects.select_related('wishlist').filter(wishlist__user=self.request.user ,product=product)

        return context

class CategoryView(ListView): 
    model = Product
    template_name = "category.html"

    def get_context_data(self, **kwargs):
        context = super(CategoryView, self).get_context_data(**kwargs)

        category = Category.objects.filter(parent=None)
        products = Product.active.all()
        # GET request ---> Catgeory
        request_category = self.request.GET.get('category', None)
        sub_category = []
        if request_category:
            sub_category= Category.objects.get(slug=request_category).get_children()
            products = products.filter(category__slug=request_category)

        # GET request ---> Sub Catgeory
        request_sub_category = self.request.GET.get('subcategory', None)
        sub_subcategory = []
        if request_sub_category:
            products = products.filter(sub_category__slug=request_sub_category)
  
        paginator = Paginator(products, 40)            
        page = self.request.GET.get('page')
        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            products = paginator.page(1)
        except EmptyPage:
            products = paginator.page(paginator.num_pages)
    

        context = {
                'sub_category':sub_category,
                'products': products,
                'category': category,
                } 
        return context





