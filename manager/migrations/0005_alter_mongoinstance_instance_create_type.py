# Generated by Django 3.2.4 on 2023-01-09 15:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("manager", "0004_auto_20230109_2215"),
    ]

    operations = [
        migrations.AlterField(
            model_name="mongoinstance",
            name="instance_create_type",
            field=models.CharField(
                choices=[("PAGE_LOGIN", "PAGE_LOGIN"), ("APIGW_CREATED", "APIGW_CREATED")],
                default="PAGE_LOGIN",
                max_length=128,
                verbose_name="实例创建类型",
            ),
        ),
    ]
