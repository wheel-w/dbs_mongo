from django.utils.decorators import method_decorator
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from account.decorators import login_exempt


@method_decorator(login_exempt, name="dispatch")
class LoginExemptTokenObtainPairView(TokenObtainPairView):
    pass


@method_decorator(login_exempt, name="dispatch")
class LoginExemptTokenRefreshView(TokenRefreshView):
    pass


@method_decorator(login_exempt, name="dispatch")
class LoginExemptTokenVerifyView(TokenVerifyView):
    pass
