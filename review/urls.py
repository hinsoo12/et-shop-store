from django.urls import path
from .views import ReviewView,add_review, submit_review

urlpatterns = [
    path('review/',ReviewView.as_view(), name="review"),
    path('add_review/<int:id>',add_review, name="add_review"),
    path('review-products/<int:product_id>/submit_review/', submit_review, name='submit_review'),
]   
