from django.shortcuts import render
from django.urls import reverse
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect, get_object_or_404

from .models import OrderItem
from .forms import OrderCreateForm
from .tasks import order_created
from cart.cart import Cart
from .models import Order

def order_create(request):

    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)

        if form.is_valid():
            order = form.save()
            # Create OrderItem record for each item in cart
            for item in cart:
                orderItem = OrderItem.objects.create(order=order,
                                                     product=item['product'],
                                                     price=item['price'],
                                                     quantity=item['quantity'])

            # clear items from cart
            cart.clear()

            # launch asynchronous task; email user confirming order.
            order_created.delay(order.id)
            # set order id into session
            request.session['order_id'] = order.id
            # redirect for payment
            return redirect(reverse('payment:process'))

    else:
        form = OrderCreateForm()

    return render(request,
                  'orders/order/create.html',
                  {'cart':cart,
                   'form': form})

@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request,
                  'admin/orders/order/detail.html',
                  {'order': order})
