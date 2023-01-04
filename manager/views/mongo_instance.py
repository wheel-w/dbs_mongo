from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from manager.models import MongoInstance
from manager.permissions.mongo_instance_permission import MongoInstancePermission
from manager.serializers.mongo_instance_serializer import (
    MongoInstanceLoginListSerializer,
    MongoInstanceSerializer,
    MongoInstanceSessionAuthSerializer,
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

    @swagger_auto_schema(
        method="POST", operation_summary="user_session_auth", request_body=MongoInstanceSessionAuthSerializer
    )
    @action(detail=False, methods=["POST"])
    def user_session_auth(self, request):
        serializer = MongoInstanceSessionAuthSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        session = serializer.save()
        return Response(
            {
                "id": session.session_id,
            }
        )

    @swagger_auto_schema(
        method="POST", operation_summary="app_session_auth", request_body=MongoInstanceSessionAuthSerializer
    )
    @action(detail=False, methods=["POST"])
    def app_session_auth(self, request):
        serializer = MongoInstanceSessionAuthSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        session = serializer.save()
        return Response(
            {
                "id": session.session_id,
            }
        )
