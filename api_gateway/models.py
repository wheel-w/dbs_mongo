from django.db import models


class ApplicationInfoManager(models.Manager):
    def verify_app(self, app_code, app_secret):
        app = self.get_queryset().filter(app_code=app_code, app_secret=app_secret).first()
        if not app:
            return False
        return True


class ApplicationInfo(models.Model):
    app_code = models.CharField(verbose_name="应用code", primary_key=True, max_length=16)
    app_name = models.CharField(verbose_name="应用名称", max_length=32)
    app_principal = models.CharField(verbose_name="应用接口人", max_length=32)
    app_secret = models.CharField(verbose_name="应用secret", max_length=64)
    created_by = models.CharField(verbose_name="应用创建人", max_length=32)
    update_time = models.DateTimeField(auto_now=True)
    objects = ApplicationInfoManager()

    class Meta:
        db_table = "apigw_application_info"
        ordering = ["-update_time"]
