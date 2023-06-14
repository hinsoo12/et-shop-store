from .models import Pages

def pages(request):
    return {'pages': Pages.objects.all().order_by('id')}
