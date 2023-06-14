from django.shortcuts import render
from django.views.generic import ListView , DetailView
from product.models import Product, Category
from .models import Pages , Sliders
from django.db.models import Q

class Home(ListView):
    template_name = "home.html"
    model = Product

    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['products'] = Product.active.all()
        context['sliders'] = Sliders.objects.all()
        return context 

class PageDetail(DetailView):
    model = Pages
    template_name = "page.html"

def search_product(request):
    query = request.GET.get('q') # Get the query parameter from the URL
    products = Product.objects.filter(Q(title__icontains=query) | Q(brand__icontains=query)) # Filter the products by name or brand that contain the query
    context = {
        'query': query,
        'products': products,
    }
    return render(request, 'search.html', context) # Render the search template with the context
