"""
Django settings for dbs_mongodb project.

Generated by 'django-admin startproject' using Django 3.2.4.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
import os
from pathlib import Path

from common.env import settings

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-e+00dp&69sgsw8l2wz0z5(%^lfs=_8(4b2v!3vyk8tme&r0k0j"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = settings.RUNTIME_ENVIRONMENT == "dev"

ALLOWED_HOSTS = [s for s in settings.CORS_ALLOWED_HOSTS.split(",") if s]
# 跨域配置
CORS_ORIGIN_WHITELIST = [f"http://{s}" for s in settings.CORS_ALLOWED_HOSTS.split(",") if s]
CORS_ORIGIN_WHITELIST += [f"https://{s}" for s in settings.CORS_ALLOWED_HOSTS.split(",") if s]
CORS_ALLOW_CREDENTIALS = True

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "manager",
    "account",
    "rest_framework",
    "drf_yasg",
    "corsheaders",
    "api_gateway",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "common.middlewares.TraceIDInjectMiddleware",
    "api_gateway.middlewares.ApplicationInjectMiddleware",
    "account.middlewares.LoginRequiredMiddleware",
]

# csrf config
CSRF_COOKIE_DOMAIN = settings.CSRF_COOKIE_DOMAIN or None
CSRF_COOKIE_NAME = "dbs_mongo-csrftoken"

ROOT_URLCONF = "urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "wsgi.application"

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# account
LOGIN_CACHE_EXPIRED = 60
AUTH_USER_MODEL = "account.User"
AUTHENTICATION_BACKENDS = ("account.backends.UserBackend",)

# drf 设置
REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": [
        "common.drf.renderers.StandardResponseRenderer",
        "rest_framework.renderers.BrowsableAPIRenderer",
    ],
}

# static
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
# cache
CACHES = {
    "db": {
        "BACKEND": "django.core.cache.backends.db.DatabaseCache",
        "LOCATION": "django_cache",
    },
    "login_db": {
        "BACKEND": "django.core.cache.backends.db.DatabaseCache",
        "LOCATION": "account_cache",
    },
    "dummy": {"BACKEND": "django.core.cache.backends.dummy.DummyCache"},
}
CACHES["default"] = CACHES["dummy"]

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = []

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = "zh-hans"
TIME_ZONE = "Asia/Shanghai"
USE_TZ = False

USE_I18N = True

USE_L10N = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = "/static/"

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# 日志配置
log_dir = BASE_DIR.parent / "dbs_mongodb_logs"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "[trace_id={trace_id}] {levelname} {asctime} {module} {process:d} {thread:d} {message}",
            "style": "{",
        },
        "simple": {
            "format": "[trace_id={trace_id}] {levelname} {message}",
            "style": "{",
        },
    },
    "filters": {
        "require_debug_true": {
            "()": "django.utils.log.RequireDebugTrue",
        },
        "trace_id_inject_filter": {"()": "common.utils.log.TraceIDInjectFilter"},
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "filters": ["require_debug_true", "trace_id_inject_filter"],
            "formatter": "simple",
        },
        "mongo-info": {
            "level": "INFO",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": log_dir / "info.log",
            "filters": ["trace_id_inject_filter"],
            "maxBytes": 1024 * 1024 * 100,
            "backupCount": 5,
        },
        "mongo-error": {
            "level": "ERROR",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": log_dir / "error.log",
            "filters": ["trace_id_inject_filter"],
            "maxBytes": 1024 * 1024 * 100,
            "backupCount": 5,
        },
    },
    "loggers": {
        "mongo": {"handlers": ["mongo-info", "mongo-error", "console"], "level": "INFO", "propagate": True},
    },
}
