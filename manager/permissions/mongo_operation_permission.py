from rest_framework import permissions

from manager.models import MongoInstance


class MongoOperationPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        instance_id = view.kwargs.get("pk")
        if not instance_id:
            return False
        dbs_user_rtx = MongoInstance.objects.get_dbs_user_rtx(instance_id)
        return dbs_user_rtx == request.user.username

    def has_object_permission(self, request, view, obj):
        return True
