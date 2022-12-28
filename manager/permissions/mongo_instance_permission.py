from rest_framework import permissions


class MongoInstancePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        return obj.dbs_user_rtx == request.user.username
