# -*- coding: utf-8 -*-

from django.contrib import admin
from django.urls import include, path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Dbd Mongo API",
        default_version="v1",
        description="Dbs Mongo API",
    ),
    public=True,
    permission_classes=[permissions.IsAdminUser],
)
urlpatterns = [
    path(r"django_admin/", admin.site.urls),
    path(r"api/", include("manager.urls")),
    path(r"account/", include("account.urls")),
    re_path(r"^swagger(?P<format>\.json|\.yaml)$", schema_view.without_ui(cache_timeout=0), name="schema-json"),
    re_path(r"^$", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    re_path(r"^redoc/$", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]
