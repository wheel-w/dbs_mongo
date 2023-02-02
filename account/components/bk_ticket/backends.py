import logging

import requests
from django.contrib.auth.backends import ModelBackend

from account import get_user_model
from common.env import settings

logger = logging.getLogger("mongo")


class UserBackend(ModelBackend):
    def authenticate(self, request=None, bk_ticket=None):
        if not bk_ticket:
            return None

        result, user_info = self.verify_bk_ticket(bk_ticket, request)
        if not result:
            return None

        user_model = get_user_model()
        user, _ = user_model.objects.get_or_create(username=user_info["username"])
        user.nickname = user_info["username"]
        user.avatar_url = user_info["avatar_url"]
        user.save()
        return user

    @staticmethod
    def verify_bk_ticket(bk_ticket, request=None):
        ulr = "{}/user/get_info/?bk_ticket={}".format(settings.LOGIN_AUTH_URL, bk_ticket)
        try:
            response = requests.get(ulr).json()
            ret = response.get("ret")
            if ret == 0:
                return True, response["data"]
        except Exception:
            logger.exception("bk_ticket 验证异常")
            return False, None
