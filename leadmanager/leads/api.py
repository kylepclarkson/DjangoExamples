from rest_framework import viewsets, permissions

from .serializers import LeadSerializer
from .models import Lead


class LeadViewSet(viewsets.ModelViewSet):
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    serializer_class = LeadSerializer

    # override. Get leads for user.
    def get_queryset(self):
        return self.request.user.leads.all()

    # override. Create lead using user.
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
