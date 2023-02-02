from django.http import JsonResponse

from account.utils import build_redirect_url, resolve_login_url
from common.env import settings


class ResponseHandler(object):
    def build_ajax_401_response(self, request):
        _next = request.build_absolute_uri()
        _login_url = build_redirect_url(
            _next,
            resolve_login_url("{}/plain/?size=full".format(settings.LOGIN_AUTH_URL), request),
            "c_url",
        )
        context = {
            "code": 1,
            "result": False,
            "message": "用户认证失败，请先进行登录",
            "login_url": _login_url,
        }

        return JsonResponse(context, status=401)

    def build_jwt_401_response(self, request):
        context = {
            "code": 1,
            "result": False,
            "message": "用户认证失败，请先进行登录",
            "login_url": "xxx",
        }

        return JsonResponse(context, status=401)
