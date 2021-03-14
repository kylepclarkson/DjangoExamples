from django import forms
from .models import Order


class OrderCreateForm(forms.ModelForm):

    """ A form presented to the user when they create a new order. """
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'address', 'postal_code', 'city']
