from rest_framework import serializers

from manager.client import DbsMongoClient
from manager.constants import InstanceCreateType
from manager.models import MongoInstance


class MongoInstanceLoginListSerializer(serializers.ModelSerializer):
    class Meta:
        model = MongoInstance
        fields = ["instance_id", "instance_name"]


class MongoInstanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = MongoInstance
        fields = "__all__"
        extra_kwargs = {
            "instance_id": {"read_only": True},
            "update_time": {"read_only": True, "format": "%Y-%m-%d %H:%M:%S"},
            "dbs_user_rtx": {
                "read_only": True,
            },
            "db_password": {
                "write_only": True,
            },
            "instance_create_type": {
                "read_only": True,
            },
            "is_show": {"write_only": True},
            "auth_source": {"default": "admin"},
            "auth_mechanism": {"default": "DEFAULT"},
            "db_port": {"default": 27017},
        }

    def validate(self, data):
        if self.partial:
            return data

        with DbsMongoClient(instance_kwargs=data) as mongo_client:
            result, message = mongo_client.dispatch("test_connection")
            if not result:
                raise serializers.ValidationError(message)
        return data

    def create(self, validated_data):
        validated_data["instance_create_type"] = InstanceCreateType.PAGE_LOGIN
        instance = MongoInstance.objects.create_instance(validated_data)
        return instance


class MongoInstanceSessionAuthSerializer(serializers.Serializer):
    session_timeout = serializers.IntegerField(label="会话有效时长", default=60 * 60 * 4)
    dbs_user_rtx = serializers.CharField(label="会话链接生效用户")
