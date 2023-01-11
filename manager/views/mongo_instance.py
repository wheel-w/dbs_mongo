import datetime

from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from common.env import settings
from common.utils import local
from manager.constants import InstanceCreateType
from manager.models import MongoInstance, MongoInstanceSessionInfo
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

    @action(detail=True, methods=["GET"])
    def session_instance(self, request, pk):
        session_qs = MongoInstanceSessionInfo.objects.all()
        session = get_object_or_404(session_qs, pk=pk)
        now = datetime.datetime.now()
        if (now - session.expire_at).total_seconds() > 0:
            return Response("session link is expired", exception=True)
        self.check_object_permissions(request, session)
        return Response({"instance_id": session.instance_id})

    def list(self, request, *args, **kwargs):
        app_code = local.get_app_code()
        if app_code:
            instance_create_type = InstanceCreateType.APIGW_CREATED
        else:
            instance_create_type = InstanceCreateType.PAGE_LOGIN
        queryset = self.filter_queryset(self.get_queryset()).filter(
            is_show=True, dbs_user_rtx=local.get_request_username(), instance_create_type=instance_create_type
        )

        serializer = MongoInstanceLoginListSerializer(queryset, many=True)
        return Response(serializer.data)

    def perform_destroy(self, instance):
        instance.is_show = False
        instance.save()

    @swagger_auto_schema(
        method="POST", operation_summary="user_session_auth", request_body=MongoInstanceSessionAuthSerializer
    )
    @action(detail=True, methods=["POST"])
    def session_link(self, request, pk):
        instance = self.get_object()
        source_instance_id = instance.pk
        serializer = MongoInstanceSessionAuthSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data
        instance.pk = None
        instance.is_show = False
        instance.dbs_user_rtx = data["dbs_user_rtx"]
        instance.instance_create_type = InstanceCreateType.PAGE_LOGIN
        instance.created_by = local.get_request_username()
        instance.save()
        session_info = {
            "instance_id": instance.pk,
            "source_instance_id": source_instance_id,
            "expire_at": datetime.datetime.now() + datetime.timedelta(seconds=data["session_timeout"]),
            "dbs_user_rtx": data["dbs_user_rtx"],
        }
        session = MongoInstanceSessionInfo.objects.create(**session_info)
        session_link = "{}?session_id={}".format(settings.FRONTEND_LOGIN_URL, session.session_id)
        return Response({"session_link": session_link, "expire_at": session.expire_at.strftime("%Y-%m-%d %H:%M:%S")})
