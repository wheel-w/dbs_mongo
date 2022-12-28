from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from manager.models import MongoInstance
from manager.permissions.mongo_instance_permission import MongoInstancePermission
from manager.serializers.mongo_instance_serializer import (
    MongoInstanceLoginListSerializer,
    MongoInstanceSerializer,
)


class MongoInstanceViewSet(ModelViewSet):
    queryset = MongoInstance.objects.all()
    serializer_class = MongoInstanceSerializer
    permission_classes = [MongoInstancePermission]
    http_method_names = ["get", "post", "patch", "delete", "head", "options", "trace"]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset()).filter(is_show=True, dbs_user_rtx=request.user.username)

        serializer = MongoInstanceLoginListSerializer(queryset, many=True)
        return Response(serializer.data)

    def perform_destroy(self, instance):
        instance.is_show = False
        instance.save()
