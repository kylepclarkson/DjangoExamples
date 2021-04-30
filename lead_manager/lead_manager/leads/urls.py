from rest_framework import routers
from .api import LeadViewSet

"""
    Use LeadViewSet to manage urls with /api/leads
"""

router = routers.DefaultRouter()
router.register('api/leads', LeadViewSet, 'leads')

urlpatterns = router.urls