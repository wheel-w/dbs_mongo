from django.utils.decorators import method_decorator
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from account import get_user_model
from account.components.default.serializers import (
    UserChangePasswordSerializer,
    UserRegisterSerializer,
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


@method_decorator(login_exempt, name="dispatch")
class UserRegisterView(generics.GenericAPIView):
    serializer_class = UserRegisterSerializer

    def post(self, request):
        user_model = get_user_model()
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data["username"]
        password = serializer.validated_data["password"]
        user_model.objects.create_user(username, password)

        return Response()


class UserChangePasswordView(generics.GenericAPIView):
    serializer_class = UserChangePasswordSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        user = request.user
        old_password = serializer.validated_data["old_password"]
        new_password = serializer.validated_data["new_password"]
        result = user.check_password(old_password)
        if not result:
            return Response(data="password is error", exception=True)

        user.set_password(new_password)
        user.save()
        return Response()
