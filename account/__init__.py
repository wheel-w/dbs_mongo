from django.contrib import auth
from django.utils.module_loading import import_string

from common.env import settings


def load_model(backend):
    path = "account.components.{backend}.models.UserProxy".format(backend=backend)
    return import_string(path)


def get_user_model():
    """
    返回平台对应版本 User Proxy Model
    """
    return load_model(settings.LOGIN_ACCOUNT_COMPONENT_NAME)


auth.get_user_model = get_user_model
