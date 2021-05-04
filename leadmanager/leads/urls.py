from rest_framework import routers
from .api import LeadViewSet

# use rest_framework to handle routes.

router = routers.DefaultRouter()
router.register('api/leads', LeadViewSet, 'leads')

# add to patterns
urlpatterns = router.urls

