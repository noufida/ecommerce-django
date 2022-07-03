from .models import Cart,CartItem
from .views import _cart_id
from  item.models import Wish

def counter(request):
    cart_count = 0
    if 'admin' in request.path:
        return()
    else:
        try:
            cart = Cart.objects.filter(cart_id = _cart_id(request))
            if request.user.is_authenticated:
                cart_items = CartItem.objects.all().filter(user=request.user)
            else:
                cart_items = CartItem.objects.all().filter(cart=cart[:1])
            for cart_item in cart_items:
                cart_count += cart_item.quantity
        except Cart.DoesNotExist:
            cart_count = 0
    return dict(cart_count=cart_count)


def counter_wish(request):
    wishlist_count = 0
    if 'admin' in request.path:
        return()
    else:
        try:
            wishlilst = Wish.objects.filter(user = request.user)            
            wishlist_count = wishlilst.count()
            
        except:
            wishlist_count = 0
    return dict(wishlist_count=wishlist_count)