from django.urls import path

from .views import *

urlpatterns = [
    path('',  BlogIndex.as_view(), name='blog-index'),

]
app_name = 'blog'
