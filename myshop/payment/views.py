from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings

import braintree

from orders.models import Order


# braintree gateway
gateway = braintree.BraintreeGateway(settings.BRAINTREE_CONF)


def payment_process(request):
    """ Get order from session. If request method is POST, attempt to create a
     payment. If successful update order instance."""

    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)
    total_cost = order.get_total_cost()

    if request.method == 'POST':
        nonce = request.POST.get('payment_method_nonce', None)
        # create and submit transaction
        result = gateway.transaction.sale({
            'account': f'{total_cost: 2f}',
            'payment_method_nonce': nonce,
            'options': {
                'submit_for_settlement': True
            }
        })

        if result.is_success:
            order.paid = True
            order.braintree_id = result.transaction.id
            order.save()
            return redirect('payment:done')
        else:
            return redirect('payment:canceled')
    else:
        client_token = gateway.client_token.generate()
        context = {
            'order': order,
            'client_token': client_token
        }
        return render(request,
                      'payment/process.html',
                      context)

