from django.urls import path

from . import views

urlpatterns = [
    path('', views.super_basic_index, name='index'),
    path('123/', views.super_basic_index, name='index123')
]
