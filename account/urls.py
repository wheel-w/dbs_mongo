from django.conf.urls import url

from account import views

app_name = "account"  # pylint: disable=invalid-name

urlpatterns = [
    url(r"^get_user_info/$", views.get_user_info, name="get_user_info"),
    url(r"^get_csrf_token/$", views.get_csrf_token, name="get_csrf_token"),
    url(r"^refresh_superuser/$", views.refresh_superuser, name="refresh_superuser"),
]
