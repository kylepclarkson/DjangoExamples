from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to allow only owners of a code snippet
    to edit it.
    """

    def has_object_permission(self, request, view, obj):

        # Allow GET, HEAD, or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permission is given only if user created snippet.
        return obj.owner == request.user