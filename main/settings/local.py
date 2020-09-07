from .base import *
from .logging import ConfigureLogger

DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'LOCAL_SECRET_KEY'

LOGGING_DIR = os.path.join(BASE_DIR, 'logs')
LOGGING_LEVEL = 'DEBUG'

ConfigureLogger(log_level=LOGGING_LEVEL, logging_dir=LOGGING_DIR, django_modules=PROJECT_APPS)

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# DISABLE SENTRY
RAVEN_CONFIG['dsn'] = ''
RAVEN_CONFIG['environment'] = 'local'

# GOOGLE RECAPTCHA FAKE KEYS
RECAPTCHA_PUBLIC_KEY = '6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI'
RECAPTCHA_PRIVATE_KEY = '6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe'

SILENCED_SYSTEM_CHECKS = ['captcha.recaptcha_test_key_error']

CORS_ORIGIN_WHITELIST = [
    'http://127.0.0.1:9999',
    'http://localhost:9999',
]

INTERNAL_IPS = [
    '127.0.0.1',
]

INSTALLED_APPS += [
    'debug_toolbar',
]

MIDDLEWARE += [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

try:
    from .local_settings import *
except ImportError:
    pass
