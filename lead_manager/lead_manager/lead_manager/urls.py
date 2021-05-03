from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('frontend.urls')), #load frontend before API
    path('', include('leads.urls')),
]
