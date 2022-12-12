import logging

from django.conf import settings
from django.contrib import auth
from django.core.cache import caches
from django.utils.deprecation import MiddlewareMixin

from account.components.bk_ticket.forms import AuthenticationForm
from account.handlers.response import ResponseHandler

logger = logging.getLogger("mongo")
cache = caches["login_db"]


class LoginRequiredMiddleware(MiddlewareMixin):
    def process_view(self, request, view, args, kwargs):

        # 登录豁免
        if getattr(view, "login_exempt", False):
            return None

        user = self.authenticate(request)
        if user:
            return None

        handler = ResponseHandler()
        return handler.build_ajax_401_response(request)

    def process_response(self, request, response):
        return response

    def authenticate(self, request):
        form = AuthenticationForm(request.COOKIES)
        if not form.is_valid():
            return None

        bk_ticket = form.cleaned_data["bk_ticket"]
        session_key = request.session.session_key
        # 确认 cookie 中的 ticket 和 cache 中的是否一致
        if session_key:
            cache_session = cache.get(session_key)
            is_match = cache_session and bk_ticket == cache_session.get("bk_ticket")
            if is_match and request.user.is_authenticated:
                return request.user
        user = auth.authenticate(request=request, bk_ticket=bk_ticket)
        if user is not None and user.username != request.user.username:
            auth.login(request, user)
        if user is not None and request.user.is_authenticated:
            # 登录成功，重新调用自身函数，即可退出
            cache.set(session_key, {"bk_ticket": bk_ticket}, settings.LOGIN_CACHE_EXPIRED)
            return self.authenticate(request)
        return user
