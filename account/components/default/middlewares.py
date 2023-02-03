import logging

from django.contrib import auth
from django.utils.deprecation import MiddlewareMixin
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken

from account.components.default.forms import AuthenticationForm
from account.handlers.response import ResponseHandler
from common.utils import local

logger = logging.getLogger("mongo")


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
        form = AuthenticationForm(request.COOKIES)
        if not form.is_valid():
            return None

        dbs_token = form.cleaned_data["dbs_token"]

        validated_token = self.get_validated_token(dbs_token)

        user = self.get_user(validated_token)
        if user is not None and user.username != request.user.username:
            auth.login(request, user)

        return user
