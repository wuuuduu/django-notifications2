from .base import *
from .logging import ConfigureLogger

ConfigureLogger(log_level=LOGGING_LEVEL, logging_dir=LOGGING_DIR, django_modules=PROJECT_APPS)

REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] = [
    'rest_framework.renderers.JSONRenderer',
]

ALLOWED_HOSTS = [
    'api.example.com'
]

RAVEN_CONFIG['environment'] = 'prod'

CORS_ORIGIN_WHITELIST = [
    'https://example.com',
    'https://www.example.com',
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

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'localhost'
EMAIL_HOST_USER = 'django@localhost'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_TIMEOUT = 30
EMAIL_HOST_PASSWORD = 'EmailPassword123'
