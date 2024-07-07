from .models import Order,Wishlist


def cart_item_count(request):
    if request.user.is_authenticated:
        cart = Order.objects.filter(user=request.user, paid_status=False).first()
        if cart:
            distinct_products = cart.items.values('product_id', 'size_id').distinct()
            return {'cart_item_count': distinct_products.count()}
    return {'cart_item_count': 0}


def wishlist_count(request):
    if request.user.is_authenticated:
        count = Wishlist.objects.filter(user=request.user).count()
    else:
        count = 0
    return {'wishlist_count': count}
