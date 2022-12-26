from _thread import get_ident

from werkzeug.local import Local as _Local

wz_local = _Local()


class Singleton:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls._instance, cls):
            cls._instance = object.__new__(cls, *args, **kwargs)
            return cls._instance
        self = object.__new__(cls, *args, **kwargs)
        object.__setattr__(self, "__storage__", {})
        object.__setattr__(self, "__ident_func__", get_ident)
        return self


class Local(Singleton):
    """
    local对象
    必须配合中间件RequestProvider使用
    """

    @property
    def request_username(self):
        return getattr(wz_local, "request_username", "admin")

    @request_username.setter
    def request_username(self, value):
        """
        设置全局request对象
        """
        setattr(wz_local, "request_username", value)


local = Local()
