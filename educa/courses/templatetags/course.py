from django import template

"""
A custom template filter use dby content_list.html to get model name for objects
from the model's Meta class.
"""

register = template.Library()

@register.filter
def model_name(obj):
    try:
        return obj._meta.model_name
    except AttributeError:
        return None