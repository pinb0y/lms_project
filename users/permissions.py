from rest_framework import permissions


class IsModerator(permissions.BasePermission):
    massage = "У вас нет прав на это!"

    def has_permission(self, request, view):
        return request.user.groups.filter(name="moderator").exists()


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.owner if hasattr(obj, 'owner') else False