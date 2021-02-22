
from django.contrib import admin
from django.urls import path

from .views import (
    home,
    products,
    customer,
)

urlpatterns = [
    path('home/', home, ),
    path('products/', products),
    path('customer/', customer)
]