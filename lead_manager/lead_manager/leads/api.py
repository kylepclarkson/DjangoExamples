from .models import Lead
from rest_framework import viewsets, permissions
from .serializers import LeadSerializer


# Lead Viewset
"""
    Create CRUD methods for interacting with Lead table.
"""

class LeadViewSet(viewsets.ModelViewSet):
    # get all Leads
    queryset = Lead.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = LeadSerializer
