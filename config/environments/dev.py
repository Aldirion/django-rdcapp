from config.components.base import *

DEBUG = True

ALLOWED_HOSTS = ["*"]

MIDDLEWARE += [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

INSTALLED_APPS += [
    'debug_toolbar',
]

INTERNAL_IPS += [
    '127.0.0.1:8000',
]