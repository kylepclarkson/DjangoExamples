from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
import braintree

from orders.models import Order

# instantiate Braintree payment gateway.
gateway = braintree.BraintreeGateway(settings.BRAINTREE_CONF)

def payment_process(request):

    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)

    total_cost = order.get_total_cost()

    if request.method == 'POST':

        # get nonce token from braintree.
        nonce = request.POST.get('payment_method_nonce', None)

        # create and send transaction.
        result = gateway.transaction.sale({
            'amount': f'{total_cost:.2f}',
            'payment_method_nonce': nonce,
            'options': {
                'submit_for_settlement': True # transaction automatically submitted for settlement.
            }
        })

        if result.is_success:
            # Update order entry of db.
            order.paid = True
            order.braintree_id = result.transaction.id
            order.save()
            return redirect('payment:done')
        else:
            return redirect('payment:canceled')

    else:
        # generate token
        client_token = gateway.client_token.generate()

        return render(request,
                      'payment/process.html',
                      {'order': order,
                       'client_token': client_token})

def payment_done(request):
    return render(request, 'payment/done.html')

def payment_canceled(request):
    return render(request, 'payment/canceled.html')
