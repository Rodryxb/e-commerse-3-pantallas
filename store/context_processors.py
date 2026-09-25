from .models import Cart

def cart_count(request):
    if request.user.is_authenticated:
        try:
            count = sum(item.quantity for item in request.user.cart.items.all())
            return {'cart_items_count': count}
        except Cart.DoesNotExist:
            return {'cart_items_count': 0}
    return {'cart_items_count': 0}

def active_store(request):
    return {'active_store': request.session.get('active_store', 'tenis')}
