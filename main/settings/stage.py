from .base import *
from .logging import ConfigureLogger

LOGGING_LEVEL = 'INFO'

ConfigureLogger(log_level=LOGGING_LEVEL, logging_dir=LOGGING_DIR, django_modules=PROJECT_APPS)

REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] = [
    'rest_framework.renderers.JSONRenderer',
]

ALLOWED_HOSTS = [
    'api.stage.example.com'
]

RAVEN_CONFIG['environment'] = 'stage'

CORS_ORIGIN_WHITELIST = [
    'https://stage.example.com',
    'https://www.stage.example.com',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('DATABASES_NAME'),
        'USER': os.getenv('DATABASES_USER'),
        'PASSWORD': os.getenv('DATABASES_PASSWORD'),
        'HOST': os.getenv('DATABASES_HOST'),
        'PORT': os.getenv('DATABASES_PORT'),
        'OPTIONS': {'charset': 'utf8mb4'},
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}
