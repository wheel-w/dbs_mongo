import json
import time

from django.contrib.auth import logout as default_logout
from django.http import JsonResponse
from django.middleware import csrf

from account import get_user_model
from account.decorators import login_exempt
from account.models import User
from common.env import settings


def get_user_info(request):
    return JsonResponse(
        {
            "code": 0,
            "result": True,
            "data": {
                "id": request.user.id,
                "username": request.user.username,
                "timestamp": time.time(),
            },
            "message": "ok",
        }
    )


def get_csrf_token(request):
    """
    前端获取csrf_token接口
    """
    csrf_token = csrf.get_token(request)
    return JsonResponse(
        {
            "code": 0,
            "result": True,
            "data": {
                "csrf_token": csrf_token,
            },
            "message": "ok",
        }
    )


def refresh_superuser(request):
    """
    动态初始化superuser
    """
    superuser_list = [s for s in settings.SUPERUSERS.split(",") if s]
    for name in superuser_list:
        User.objects.update_or_create(
            username=name,
            defaults={"is_staff": True, "is_active": True, "is_superuser": True},
        )

    return JsonResponse(
        {
            "code": 0,
            "result": True,
            "message": "ok",
        }
    )


@login_exempt
def register(request):
    user_model = get_user_model()
    body = json.loads(request.body)
    username = body["username"]
    password = body["password"]
    user_model.objects.create_user(username, password)
    return JsonResponse(
        {
            "code": 0,
            "result": True,
            "message": "register success",
        }
    )


def logout(request):
    default_logout(request)
    return JsonResponse(
        {
            "code": 0,
            "result": True,
            "message": "logout success",
        }
    )
