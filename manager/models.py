import uuid

from django.db import models

from common.utils.aes_cipher import aes_cipher
from common.utils.local import local
from manager.constants import InstanceCreateType


class MongoInstanceManager(models.Manager):
    def create_instance(self, instance_kwargs):
        if "db_password" in instance_kwargs:
            instance_kwargs["db_password"] = aes_cipher.encrypt(instance_kwargs["db_password"])

        if "dbs_user_rtx" not in instance_kwargs:
            instance_kwargs["dbs_user_rtx"] = local.request_username

        query_kwargs = {
            "db_host": instance_kwargs["db_host"],
            "db_port": instance_kwargs.get("db_port"),
            "instance_create_type": instance_kwargs.get("instance_create_type"),
            "dbs_user_rtx": instance_kwargs["dbs_user_rtx"],
        }
        query_result = self.get_queryset().filter(**query_kwargs).first()
        if query_result:
            for k, v in instance_kwargs.items():
                setattr(query_result, k, v)
            query_result.save()
            return query_result
        return super().create(**instance_kwargs)

    def get_instance(self, instance_id):
        return self.get_queryset().filter(pk=uuid.UUID(instance_id)).first()

    def get_dbs_user_rtx(self, instance_id):
        qs = self.get_queryset().values("dbs_user_rtx").filter(pk=uuid.UUID(instance_id)).first()
        if not qs:
            return None
        return qs.get("dbs_user_rtx")


class MongoInstance(models.Model):
    # mongo认证方式
    MONGO_AUTH_MECHANISM_CHOICES = (
        ("SCRAM-SHA-256", "SCRAM-SHA-256"),
        ("MONGODB-X509", "MONGODB-X509"),
        ("MONGODB-CR", "MONGODB-CR"),
        ("PLAIN", "PLAIN"),
        ("MONGODB-AWS", "MONGODB-AWS"),
        ("GSSAPI", "GSSAPI"),
        ("DEFAULT", "DEFAULT"),
        ("SCRAM-SHA-1", "SCRAM-SHA-1"),
    )

    # 实例创建认证类型
    INSTANCE_CREATE_TYPE = (
        (InstanceCreateType.PAGE_LOGIN, "PAGE_LOGIN"),
        (InstanceCreateType.SESSION_AUTH, "SESSION_AUTH"),
    )

    instance_id = models.UUIDField(verbose_name="实例ID", primary_key=True, default=uuid.uuid4)
    instance_name = models.CharField(verbose_name="实例名称", max_length=128)
    instance_create_type = models.CharField(
        verbose_name="实例创建类型", choices=INSTANCE_CREATE_TYPE, default=InstanceCreateType.PAGE_LOGIN, max_length=128
    )
    db_host = models.CharField(verbose_name="数据库地址", max_length=256)
    db_port = models.IntegerField(verbose_name="数据库端口", default=27017)
    db_user = models.CharField(verbose_name="数据库用户名", max_length=128, null=True, blank=True)
    db_password = models.CharField(verbose_name="数据库密码", max_length=256, null=True, blank=True)
    auth_source = models.CharField(verbose_name="认证数据库", default="admin", max_length=128)
    auth_mechanism = models.CharField(
        verbose_name="认证方式", choices=MONGO_AUTH_MECHANISM_CHOICES, default="DEFAULT", max_length=128
    )
    update_time = models.DateTimeField(auto_now=True)
    is_show = models.BooleanField(verbose_name="实例是否显示用于登录", default=False)
    dbs_user_rtx = models.CharField(verbose_name="dbs用户名", max_length=128)

    objects = MongoInstanceManager()

    class Meta:
        db_table = "mongo_instance"
        ordering = ["-update_time"]

    def __str__(self):
        return f"{self.dbs_user_rtx}:{self.db_host}:{self.db_user}"

    @property
    def plain_password(self):
        return aes_cipher.decrypt(self.db_password)


class MongoInstanceSessionInfo(models.Model):
    session_id = models.UUIDField(verbose_name="会话ID", primary_key=True, default=uuid.uuid4)
    instance_id = models.UUIDField(verbose_name="session会话对应的实例id")
    expire_at = models.DateTimeField(verbose_name="会话过期时间")
    dbs_user_rtx = models.CharField(verbose_name="session会话生效人", max_length=128)
    callback_url = models.URLField(verbose_name="session回调审计url", max_length=256, null=True, blank=True)
    created_by = models.CharField(verbose_name="session会话创建人", max_length=128)
    update_time = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.created_by = local.request_username

        super().save(*args, **kwargs)
