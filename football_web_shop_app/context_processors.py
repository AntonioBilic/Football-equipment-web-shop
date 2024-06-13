from .models import Order,Wishlist


def cart_item_count(request):
    if request.user.is_authenticated:
        order = Order.objects.filter(user=request.user, paid_status=False).first()
        if order:
            return {'cart_item_count': order.items.count()}
    return {'cart_item_count': 0}



def wishlist_count(request):
    if request.user.is_authenticated:
        count = Wishlist.objects.filter(user=request.user).count()
    else:
        count = 0
    return {'wishlist_count': count}
