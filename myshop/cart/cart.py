from decimal import Decimal
from django.conf import settings
from shop.models import Product

class Cart(object):
    '''
    For each product added to cart by uses, store product ID, quantity, and
    price when added to cart.
    '''

    def __init__(self, request):

        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)

        if not cart:
            # Save empty cart to session
            cart = self.session[settings.CART_SESSION_ID] = {}

        self.cart = cart

    def add(self, product, quantity=1, override_quantity=False):
        '''
        Add a product to the cart or update it quantity.
        Note: Convert data to string for JSON serialization.
        '''
        product_id = str(product.id)

        # Add new item to cart
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0,
                                     'price': str(product.price)}

        # Set quantity
        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity

        # Save cart
        self.save()

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        '''
        Iterate over items in the cart and return Product instances from database.
        '''
        product_ids = self.cart.keys()
        # Get product objects
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()

        for product in products:
            cart[str(product.id)]['product'] = product

        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        # Return number of items in cart
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        # remove cart from session
        del self.session[settings.CART_SESSION_ID]
        self.save()


    def save(self):
        # Mark session as 'modified' to save it
        self.session.modified = True