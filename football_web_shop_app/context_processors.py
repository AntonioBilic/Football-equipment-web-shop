from .models import Order

def cart_item_count(request):
    if request.user.is_authenticated:
        order = Order.objects.filter(user=request.user, paid_status=False).first()
        if order:
            return {'cart_item_count': order.items.count()}
    return {'cart_item_count': 0}