from .models import Cart ,CartItem
 
def cart(request):
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
            cart_count = CartItem.objects.filter(cart=cart).count()
            return {'cart_count':cart_count}
        except:
            return {}
    else:
        return {}

