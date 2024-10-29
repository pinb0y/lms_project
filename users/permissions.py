from rest_framework import permissions


class CustomerAccessPermission(permissions.BasePermission):
    massage = "У вас нет прав на это!"
    def has_permission(self, request, view):
        return request.user.groups.filter(name="moderator").exists()