from django.contrib import admin

from manager.models import MongoInstance, MongoInstanceSessionInfo, OperationRecord


class MongoInstanceAdmin(admin.ModelAdmin):
    list_display = ["instance_id", "instance_name", "is_show", "instance_create_type", "update_time"]
    search_fields = ["instance_id", "instance_name"]


admin.site.register(MongoInstance, MongoInstanceAdmin)


class MongoInstanceSessionInfoAdmin(admin.ModelAdmin):
    list_display = ["session_id", "instance_id", "expire_at", "dbs_user_rtx", "created_by", "update_time"]
    search_fields = ["session_id", "instance_id"]


admin.site.register(MongoInstanceSessionInfo, MongoInstanceSessionInfoAdmin)


class OperationRecordAdmin(admin.ModelAdmin):
    list_display = ["trace_id", "instance_id", "api_name", "occur_time"]
    search_fields = ["trace_id", "instance_id", "api_name"]


admin.site.register(OperationRecord, OperationRecordAdmin)
