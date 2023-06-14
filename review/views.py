from django.shortcuts import render ,HttpResponseRedirect
from .models import Review
from order.models import OrderItem
from django.views.generic import ListView
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank , TrigramSimilarity
from django.db.models import Q
from django.db.models import Prefetch
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .forms import ReviewForm
class ReviewView(LoginRequiredMixin,ListView):
    model= OrderItem
    template_name = "review_list.html" 
    login_url = '/customer/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tab = self.request.GET.get('tab')
  
        reviews = Review.objects.filter(user=self.request.user)

        is_reviewed = OrderItem.objects.select_related('product').filter(item_review__in=reviews).prefetch_related(Prefetch('item_review', queryset=Review.objects.filter(user=self.request.user, parent__isnull=True)))

        review_list = OrderItem.objects.select_related('product').filter(order__user=self.request.user ,item_status="Completed").prefetch_related(Prefetch('item_review', queryset=Review.objects.filter(user=self.request.user))).exclude(id__in=is_reviewed).order_by('-created')
 
        if tab == 'history':
            review_list = is_reviewed 

        context={
            'review_list':review_list,
            'is_reviewed':is_reviewed,
        }
        return context
    

@login_required(login_url='/login/')
def add_review(request ,id):
    url = request.META.get('HTTP_REFERER')
    order_item = OrderItem.objects.get(id=id)
    content = request.POST['content']
    stars = request.POST['stars']
    Review.objects.update_or_create(user=request.user, content=content, order_item=order_item, stars=stars)    
    messages.success(request, 'Your review has been successfully sent.')
    return HttpResponseRedirect(url)

# A view that allows the user to submit a review and a rating for the product
@login_required
def submit_review(request, order_id):
    ordered_item = OrderItem.objects.get(id=order_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.order_item = ordered_item
            review.save()
            return redirect('product_detail', product_id)
        else:
            form = ReviewForm()
            context = {
            'form': form,
            'product': product,
            }
            return render(request, 'submit_review.html', context)


