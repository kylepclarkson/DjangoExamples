import json
from .models import *


def cookieCart(request):
    """ Creates order using contents of cart. """
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


def cartData(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']
        order = cookieData['order']
        items = cookieData['items']
    return {
        'cartItems': cartItems,
        'order': order,
        'items': items,
    }


def guestOrder(request, data):
    name = data['form']['name']
    email = data['form']['email']

    cookieData = cookieCart(request)
    items = cookieData['items']

    # create customer
    customer, created = Customer.objects.get_or_create(
        email=email,
    )
    customer.name = name
    customer.save()

    order = Order.objects.create(
        customer=customer,
        complete=False,
    )

    for item in items:
        # create order items, attach to order
        product = Product.objects.get(id=item['product']['id'])
        orderItem = OrderItem.objects.create(
            product=product,
            order=order,
            quantity=item['quantity']
        )
    return customer, order