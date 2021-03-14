from decimal import Decimal
from django.conf import settings
from shop.models import Product


class Cart(object):

    """
    A cart object where users can store items while browsing the site. The cart field is a dictionary
    where keys are product ids and values are dictionaries. The value dictionaries have string keys
    'quantity' and 'price' which store integers and price of item (when added to cart) respectively.

    """

    def __init__(self, request):
        """ Get (or create) cart session of user. """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # No cart instance existed in session. Create one.
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, quantity=1, override_quantity=False):
        """ Add/update a product to the cart. """
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {
                'quantity': 0,
                'price': str(product.price)
            }
        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.session_updated()

    def remove(self, product):
        """ Remove a product from the cart """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.session_updated()

    def clear(self):
        """ Remove cart from session. """
        del self.session[settings.CART_SESSION_ID]
        self.session_updated()

    def __len__(self):
        """ Return the number of items in the cart """
        return sum(item['quantity'] for item in self.cart.values())

    def __iter__(self):
        """ Return an iteration of all items in the cart. """
        products_ids = self.cart.keys()
        products = Product.objects.filter(id__in=products_ids)
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product

        for item in cart.values():
            # convert to decimal object.
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']

    def session_updated(self):
        """ Mark session as updated so it gets saved. """
        self.session.modified = True