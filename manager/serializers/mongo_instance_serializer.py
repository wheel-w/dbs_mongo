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
            "is_show": {"write_only": True},
            "auth_source": {"default": "admin"},
            "auth_mechanism": {"default": "DEFAULT"},
            "db_port": {"default": 27017},
        }

    def validate(self, data):
        if self.partial:
            return data

        if data["instance_create_type"] == InstanceCreateType.PAGE_LOGIN:
            with DbsMongoClient(instance_kwargs=data) as mongo_client:
                result, message = mongo_client.dispatch("test_connection")
                if not result:
                    raise serializers.ValidationError(message)
        return data

    def create(self, validated_data):
        instance = MongoInstance.objects.create_instance(validated_data)
        return instance
