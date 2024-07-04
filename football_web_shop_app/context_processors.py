from .models import Order,Wishlist


def cart_item_count(request):
    if request.user.is_authenticated:
        cart = Order.objects.filter(user=request.user, paid_status=False).first()
        if cart:
            return {'cart_item_count': sum(item.quantity for item in cart.items.all())}
    return {'cart_item_count': 0}


def wishlist_count(request):
    if request.user.is_authenticated:
        count = Wishlist.objects.filter(user=request.user).count()
    else:
        count = 0
    return {'wishlist_count': count}
