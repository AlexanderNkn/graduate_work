"""
"""
import os

from .base import *  # noqa: F403, WPS347


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('DJANGO_APPLICATION_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(int(os.getenv('DJANGO_DEBUG') or 0))

ALLOWED_HOSTS = (os.getenv('DJANGO_ALLOWED_HOSTS') or '').split(' ')

ENABLE_DEBUG_TOOLBAR = bool(int(os.getenv('ENABLE_DEBUG_TOOLBAR') or 0))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
        'OPTIONS': {'options': '-c search_path=public,content'},
    }
}

if DEBUG and ENABLE_DEBUG_TOOLBAR:
    INSTALLED_APPS += ['debug_toolbar']  # noqa: F405
    MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']  # noqa: F405
    # to enable debug_toolbar in nginx.
    INTERNAL_IPS = type(str('c'), (), {'__contains__': lambda *a: True})()  # noqa: WPS111

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        }
    },
    'formatters': {
        'default': {
            'format': '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]',
        },
    },
    'handlers': {
        'debug-console': {
            'class': 'logging.StreamHandler',
            'formatter': 'default',
            'filters': ['require_debug_true'],
        },
    },
    'loggers': {
        'django.db.backends': {
            'level': 'DEBUG',
            'handlers': ['debug-console'],
            'propagate': False,
        }
    },
}
