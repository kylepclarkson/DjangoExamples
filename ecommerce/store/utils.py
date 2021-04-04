import json
from .models import *


def cookieCart(request):
    # access cart data from cookie
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}

    print('Cart: ', cart)
    items = []
    order = {
        'get_cart_total': 0,
        'get_cart_items': 0,
        'shipping': False,
    }
    cartItems = order['get_cart_items']
    for key in cart:
        try:
            cartItems += cart[key]['quantity']
            product = Product.objects.get(id=key)
            total = (product.price * cart[key]['quantity'])

            order['get_cart_total'] += total
            order['get_cart_items'] += cart[key]['quantity']

            # build item information, add to items list
            item = {
                'product': {
                    'id': product.id,
                    'name': product.name,
                    'price': product.price,
                    'imageURL': product.imageUrl,
                },
                'quantity': cart[key]['quantity'],
                'get_total': total,
            }
            items.append(item)

            if product.digital == False:
                order['shipping'] = True

        except:
            # item in cart is no longer available.
            pass

    return {
        'cartItems': cartItems,
        'order': order,
        'items': items,
    }
