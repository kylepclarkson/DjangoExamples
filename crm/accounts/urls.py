
from django.contrib import admin
from django.urls import path

from .views import (
    home,
    products,
    customer,
    createOrder,
    updateOrder,
    deleteOrder
)

urlpatterns = [
    path('', home, ),
    path('home/', home, name='home'),
    path('products/', products, name='products'),
    path('customer/<str:pk>', customer, name='customer'),
    path('create_order/', createOrder, name='create_order'),
    path('update_order/<str:pk>', updateOrder, name='update_order'),
    path('delete_order/<str:pk>', deleteOrder, name='delete_order'),
]