from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings

from io import BytesIO
from celery import Task
import weasyprint

from orders.models import Order


@Task
def payment_completed(order_id):
    """ Send email when order is successfully created."""
    order = Order.objects.get(order_id)
    # todo
