from rest_framework.permissions import BasePermission

"""

"""
# Ensure that only students of a course can access its contents.
class IsEnrolled(BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.students.filter(id=request.user.id).exists()