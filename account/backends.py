from django.utils.module_loading import import_string

from common.env import settings


def load_backend(component_name):
    path = "account.components.{component_name}.backends.UserBackend".format(component_name=component_name)
    return import_string(path)


if settings.LOGIN_ACCOUNT_COMPONENT_NAME == "default":
    UserBackend = import_string("django.contrib.auth.backends.ModelBackend")
else:
    UserBackend = load_backend(settings.LOGIN_ACCOUNT_COMPONENT_NAME)
