import logging

from django.contrib import auth
from django.core.cache import caches
from django.utils.deprecation import MiddlewareMixin
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken

from account.handlers.response import ResponseHandler
from common.utils import local

logger = logging.getLogger("mongo")
cache = caches["login_db"]


class LoginRequiredMiddleware(MiddlewareMixin, JWTAuthentication):
    def process_view(self, request, view, args, kwargs):

        # 登录豁免
        if getattr(view, "login_exempt", False):
            return None
        try:
            user = self.authenticate(request)
        except InvalidToken as e:
            logger.exception(e)
            handler = ResponseHandler()
            return handler.build_jwt_401_response(request)
        if user:
            local.set_request_username(request.user.username)
            return None

        handler = ResponseHandler()
        return handler.build_jwt_401_response(request)

    def process_response(self, request, response):
        return response

    def authenticate(self, request):
        header = self.get_header(request)
        if header is None:
            return None

        raw_token = self.get_raw_token(header)
        if raw_token is None:
            return None

        validated_token = self.get_validated_token(raw_token)

        user = self.get_user(validated_token)
        if user is not None and user.username != request.user.username:
            auth.login(request, user)

        return user
