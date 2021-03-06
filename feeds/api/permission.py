from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, options):
        if request.user:
            return options.user == request.user
        return False
