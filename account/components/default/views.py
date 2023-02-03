from django.utils.decorators import method_decorator
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from account.decorators import login_exempt


@method_decorator(login_exempt, name="dispatch")
class LoginExemptTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])
        data = serializer.validated_data
        response = Response(data, status=status.HTTP_200_OK)
        response.set_cookie("dbs_token", data["access"])
        return response


@method_decorator(login_exempt, name="dispatch")
class LoginExemptTokenRefreshView(TokenRefreshView):
    pass


@method_decorator(login_exempt, name="dispatch")
class LoginExemptTokenVerifyView(TokenVerifyView):
    pass
