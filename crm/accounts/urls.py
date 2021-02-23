
from django.contrib import admin
from django.urls import path

from .views import (
    home,
    loginPage,
    registerPage,
    products,
    customer,
    createOrder,
    updateOrder,
    deleteOrder,
    logoutUser,
)

urlpatterns = [
    path('', home, ),
    path('home/', home, name='home'),
    path('login/', loginPage, name='login'),
    path('logout/', logoutUser, name='logout'),
    path('register/', registerPage, name='register'),
    path('products/', products, name='products'),
    path('customer/<str:pk>', customer, name='customer'),
    path('create_order/<str:pk>', createOrder, name='create_order'),
    path('update_order/<str:pk>', updateOrder, name='update_order'),
    path('delete_order/<str:pk>', deleteOrder, name='delete_order'),
]