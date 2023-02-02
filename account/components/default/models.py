from account.models import User as BaseUser
from account.models import UserManager as BaseUserManager


class UserProxyManager(BaseUserManager):
    pass


class UserProxy(BaseUser):
    objects = UserProxyManager()

    class Meta:
        proxy = True
