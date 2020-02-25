from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    A permission used to edit/delete posts by original author.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user == obj.author
