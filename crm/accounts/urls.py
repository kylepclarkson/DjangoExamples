
from django.contrib import admin
from django.urls import path

from .views import (
    home,
    products,
    customer,
)

urlpatterns = [
    path('home/', home, name='home'),
    path('products/', products, name='products'),
    path('customer/<str:pk>', customer, name='customer'),
]