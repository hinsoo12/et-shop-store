from django import forms
from .models import Review

# A form class that inherits from ModelForm and uses the Review model
class ReviewForm(forms.ModelForm):
    # A meta class that specifies the model and the fields to use
    class Meta:
        model = Review
        fields = ['content', 'stars']
        
    # A dictionary that defines the widgets for each field
    widgets = {
    # A select widget with choices from 1 to 5 for the rating field
    'stars': forms.Select(choices=[(i, i) for i in range(1, 6)]),
    # A text area widget with rows and columns for the comment field
    'content': forms.Textarea(attrs={'rows': 5, 'cols': 40}),
    }