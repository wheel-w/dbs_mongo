from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin

from api_gateway.models import ApplicationInfo
from common.utils import local


class ApplicationInjectMiddleware(MiddlewareMixin):
    def process_view(self, request, view, args, kwargs):
        app_code = request.META.get("HTTP_X_APP_CODE", "")
        if not app_code:
            return None

        app_secret = request.META.get("HTTP_X_APP_SECRET", "")
        result = ApplicationInfo.objects.verify_app(app_code, app_secret)
        if result:
            local.set_app_code(app_code)
            request_username = request.META.get("HTTP_X_DBS_USER_RTX", app_code)
            local.set_request_username(request_username)
            setattr(view, "login_exempt", True)
            request._dont_enforce_csrf_checks = True
        else:
            return JsonResponse(
                {
                    "result": False,
                    "message": "X-APP-CODE or X-APP-SECRET in request headers missing or incorrect",
                    "code": -1,
                    "data": None,
                },
                status=403,
            )
        return None

    def process_response(self, request, response):
        return response
