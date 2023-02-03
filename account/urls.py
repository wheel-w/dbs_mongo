from django.conf.urls import url
from django.urls import path

from account import views
from account.components.default.views import (
    LoginExemptTokenObtainPairView,
    LoginExemptTokenRefreshView,
    LoginExemptTokenVerifyView,
)

app_name = "account"  # pylint: disable=invalid-name

urlpatterns = [
    url(r"^get_user_info/$", views.get_user_info, name="get_user_info"),
    url(r"^get_csrf_token/$", views.get_csrf_token, name="get_csrf_token"),
    url(r"^refresh_superuser/$", views.refresh_superuser, name="refresh_superuser"),
    url(r"^register/$", views.register, name="register"),
    url(r"^logout/$", views.logout, name="logout"),
    path("login/", LoginExemptTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", LoginExemptTokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", LoginExemptTokenVerifyView.as_view(), name="token_verify"),
]
