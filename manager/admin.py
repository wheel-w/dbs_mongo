from django.contrib import admin

from manager.models import MongoInstance, MongoInstanceSessionInfo


class MongoInstanceAdmin(admin.ModelAdmin):
    list_display = ["instance_id", "instance_name", "is_show", "instance_create_type", "update_time"]
    search_fields = ["instance_id", "instance_name"]


admin.site.register(MongoInstance, MongoInstanceAdmin)


class MongoInstanceSessionInfoAdmin(admin.ModelAdmin):
    list_display = ["session_id", "instance_id", "expire_at", "dbs_user_rtx", "created_by", "update_time"]
    search_fields = ["session_id", "instance_id"]


admin.site.register(MongoInstanceSessionInfo, MongoInstanceSessionInfoAdmin)
