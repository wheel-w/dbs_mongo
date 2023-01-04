import datetime

from rest_framework import serializers

from manager.client import DbsMongoClient
from manager.constants import InstanceCreateType
from manager.models import MongoInstance, MongoInstanceSessionInfo


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


class MongoInstanceSessionAuthSerializer(serializers.ModelSerializer):
    session_timeout = serializers.IntegerField(label="会话有效时长", default=60 * 60 * 4)

    class Meta:
        model = MongoInstance
        fields = "__all__"
        extra_kwargs = {
            "instance_id": {"read_only": True},
            "update_time": {"read_only": True, "format": "%Y-%m-%d %H:%M:%S"},
            "db_password": {
                "write_only": True,
            },
            "is_show": {
                "read_only": True,
            },
            "instance_create_type": {
                "read_only": True,
            },
            "auth_source": {"default": "admin"},
            "auth_mechanism": {"default": "DEFAULT"},
            "db_port": {"default": 27017},
        }

    def validate(self, data):
        with DbsMongoClient(instance_kwargs=data) as mongo_client:
            result, message = mongo_client.dispatch("test_connection")
            if not result:
                raise serializers.ValidationError(message)
        return data

    def create(self, validated_data):
        validated_data["instance_create_type"] = InstanceCreateType.SESSION_AUTH
        instance = MongoInstance.objects.create_instance(validated_data)

        session_info = {
            "instance_id": instance.instance_id,
            "expire_at": datetime.datetime.now() + datetime.timedelta(seconds=validated_data["session_timeout"]),
            "dbs_user_rtx": validated_data["dbs_user_rtx"],
        }
        session = MongoInstanceSessionInfo.objects.create(**session_info)
        return session
