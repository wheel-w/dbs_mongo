from django.http import JsonResponse


class ResponseHandler(object):
    def _make_login_url(self, request):
        return "xxx"

    def build_ajax_401_response(self, request):
        context = {
            "result": False,
            "message": "用户认证失败，请先进行登录",
            "login_url": self._make_login_url,
        }

        return JsonResponse(context, status=401)
