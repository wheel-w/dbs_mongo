from urllib.parse import urlparse, urlunparse

from django.http import QueryDict
from django.shortcuts import resolve_url


def resolve_login_url(url, request=None, fix_scheme=None):
    """根据网络协议解析url"""
    if url.startswith("http://") or url.startswith("https://"):
        return url
    if fix_scheme:
        return f"{fix_scheme}://{url}"
    scheme = getattr(request, "scheme", "http")
    return f"{scheme}://{url}"


def build_redirect_url(next_url, current_url, redirect_field_name, extra_args=None):
    """
    即将访问的 CUR_URL 页面， 加上下一步要跳转的 NEXT 页面
    @param {string} next_url 页面链接，比如 http://a.com/page1/
    @param {string} current_url
    """
    resolved_url = resolve_url(current_url)

    login_url_parts = list(urlparse(resolved_url))

    querystring = QueryDict(login_url_parts[4], mutable=True)
    querystring[redirect_field_name] = next_url

    if extra_args:
        querystring.update(extra_args)

    login_url_parts[4] = querystring.urlencode(safe="/")

    return urlunparse(login_url_parts)
