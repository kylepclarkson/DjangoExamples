from celery import task, Celery
from django.core.mail import send_mail

from .models import Order

@task
def order_created(order_id):
    # Send email to user confirming order.
    order = Order.objects.get(id=order_id)
    subject = f'Order nr. {order.id}'
    message = \
        f'Dear {order.first_name}, \n\n' \
        f'You have successfully places an order.' \
        f'Your order ID is {order.id}'

    mail_set = send_mail(subject, message, 'admin@myshop.com', [order.email])

    return mail_set