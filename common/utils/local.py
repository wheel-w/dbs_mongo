import typing

from werkzeug.local import Local

__LOCAL_STORAGE = Local()


def set_request_username(request_username: str):
    __LOCAL_STORAGE.request_username = request_username


def get_request_username():
    return getattr(__LOCAL_STORAGE, "request_username", None)


def set_trace_id(trace_id: str):
    __LOCAL_STORAGE.trace_id = trace_id


def get_trace_id() -> typing.Optional[str]:
    return getattr(__LOCAL_STORAGE, "trace_id", None)


def set_app_code(app_code: str):
    __LOCAL_STORAGE.app_code = app_code


def get_app_code() -> typing.Optional[str]:
    return getattr(__LOCAL_STORAGE, "app_code", None)
