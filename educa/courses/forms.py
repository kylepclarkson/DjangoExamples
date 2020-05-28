from django import forms
from django.forms.models import inlineformset_factory
from .models import Course, Module

"""
    Form to manage modules of course.
"""
ModuleFormSet = inlineformset_factory(Course,
                                      Module,
                                      fields = ['title', 'description'],
                                      extra=2,
                                      can_delete=True)