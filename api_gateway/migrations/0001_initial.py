# Generated by Django 3.2.4 on 2023-01-09 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="ApplicationInfo",
            fields=[
                ("app_code", models.CharField(max_length=16, primary_key=True, serialize=False, verbose_name="应用code")),
                ("app_name", models.CharField(max_length=32, verbose_name="应用名称")),
                ("app_principal", models.CharField(max_length=32, verbose_name="应用接口人")),
                ("app_secret", models.CharField(max_length=64, verbose_name="应用secret")),
                ("created_by", models.CharField(max_length=32, verbose_name="应用创建人")),
                ("update_time", models.DateTimeField(auto_now=True)),
            ],
            options={
                "db_table": "apigw_application_info",
                "ordering": ["-update_time"],
            },
        ),
    ]
