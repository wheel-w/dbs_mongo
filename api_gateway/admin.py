from django.contrib import admin

from api_gateway.models import ApplicationInfo


class ApplicationInfoAdmin(admin.ModelAdmin):
    list_display = ["app_name", "app_code", "app_principal", "created_by", "update_time"]


admin.site.register(ApplicationInfo, ApplicationInfoAdmin)
