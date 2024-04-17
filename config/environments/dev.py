from config.components.base import *

DEBUG = True

ALLOWED_HOSTS = ["*"]

MIDDLEWARE += [
    'debug_toolbar.middleware.DebugToolbarMiddleware'
]

INSTALLED_APPS += [
    'debug_toolbar'
]
