from rest_framework import permissions


class UpdateOwnProfile(permissions.BasePermission):
    """Allow users to edit their own profile"""

    def has_object_permission(self, request, view, obj):
        """Check user is trying to edit their own profile"""

        # SAFE_METHODS is a tuple containing GET, OPTIONS, and HEAD
        if request.method in permissions.SAFE_METHODS:
            return True

        # If the user is trying to update their own profile, allow it
        return obj.id == request.user.id
