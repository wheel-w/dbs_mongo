# Generated by Django 3.2.4 on 2023-01-31 11:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("manager", "0009_alter_operationrecord_api_data"),
    ]

    operations = [
        migrations.AlterField(
            model_name="operationrecord",
            name="api_data",
            field=models.JSONField(verbose_name="操作请求数据"),
        ),
    ]