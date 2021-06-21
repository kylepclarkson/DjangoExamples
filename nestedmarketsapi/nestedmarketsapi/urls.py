
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.documentation import include_docs_urls

from api import views

router = DefaultRouter()
router.register('match', views.MatchViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('docs/', include_docs_urls(title='Bookings API'))
]
