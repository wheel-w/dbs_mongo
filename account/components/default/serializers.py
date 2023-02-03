from rest_framework import serializers


class UserRegisterSerializer(serializers.Serializer):
    username = serializers.CharField(label="用户名", required=True)
    password = serializers.CharField(label="密码", required=True)


class UserChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(label="旧密码", required=True)
    new_password = serializers.CharField(label="新密码", required=True)
