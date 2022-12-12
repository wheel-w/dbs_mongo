from django.utils.module_loading import import_string

from common.env import settings


def load_middleware(component_name):
    path = "account.components.{component_name}.middlewares.LoginRequiredMiddleware".format(
        component_name=component_name
    )
    return import_string(path)


LoginRequiredMiddleware = load_middleware(settings.LOGIN_ACCOUNT_COMPONENT_NAME)
