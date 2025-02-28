import os
import sys
import logging
from pathlib import Path
from datetime import timedelta

from environ import Env


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

TEST_IS_RUNNING = next(iter(sys.argv), '').endswith('pytest') or ('test' in sys.argv)

env = Env(DEBUG=(bool, False))
ENV_SCOPE = 'test' if TEST_IS_RUNNING else env.str(var='DJANGO_ENV', default='local')
env.read_env(BASE_DIR / f'envs/.env.{ENV_SCOPE}', overwrite=True)

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.str(var='SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool(var='DEBUG')

ALLOWED_HOSTS = env.list(var='ALLOWED_HOSTS', default=['*'])

CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_ORIGINS = env.list(var='CORS_ALLOWED_ORIGINS', default=['http://localhost:8000', 'http://localhost:3000'])
CSRF_TRUSTED_ORIGINS = env.list(var='CSRF_TRUSTED_ORIGINS', default=['http://127.0.0.1', 'http://localhost'])


# Application definition

INSTALLED_APPS = [
    # Core apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Third-party apps
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',  # noqa
    'drf_spectacular',
    # Local apps
    'apps.accounts.apps.AccountsConfig',
    'apps.store.apps.StoreConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': env.str(var='DB_HOST', default='localhost'),
        'PORT': env.int(var='DB_PORT', default=5432),
        'NAME': env.str(var='DB_NAME'),
        'USER': env.str(var='DB_USER', default='postgres'),
        'PASSWORD': env.str(var='DB_PASSWORD', default='postgres'),
    }
}


# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
MEDIA_URL = 'media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
FIXTURE_DIRS: list[str] = []
AUTH_USER_MODEL = 'accounts.User'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# LOG
EXCEPTIONS_LOG_FILE_COUNT = 3
EXCEPTIONS_LOG_FILE_SIZE = 2 * 1024 * 1024
EXCEPTIONS_LOG_FILE_PATH = env.str(var='EXCEPTIONS_LOG_FILE_PATH', default='logs/exceptions.log')

PERFORMANCE_LOG_FILE_COUNT = 3
PERFORMANCE_LOG_FILE_SIZE = 2 * 1024 * 1024
PERFORMANCE_LOG_FILE_PATH = env.str(var='PERFORMANCE_LOG_FILE_PATH', default='logs/performance.log')


class WarningOrErrorFilter(logging.Filter):
    def filter(self, record):
        return record.levelno in (logging.WARNING, logging.ERROR)


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
        'warning_or_error': {
            '()': WarningOrErrorFilter,
        },
    },
    'formatters': {
        'general': {
            'format': '[GENERAL] | [{levelname} {asctime}] n({name}) m({module}) | {message}',
            'style': '{',
        },
        'exception': {
            'format': '[EXCEPTION] | [{levelname} {asctime}] n({name}) m({module}) | {message}',
            'style': '{',
        },
    },
    'handlers': {
        'stdout_exception': {
            'class': 'logging.StreamHandler',
            'stream': sys.stdout,
            'filters': ['warning_or_error'],
            'formatter': 'exception',
        },
        'file_exceptions': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': EXCEPTIONS_LOG_FILE_PATH,
            'maxBytes': EXCEPTIONS_LOG_FILE_SIZE,
            'backupCount': EXCEPTIONS_LOG_FILE_COUNT,
            'filters': ['warning_or_error'],
            'formatter': 'exception',
        },
        'general': {
            'class': 'logging.StreamHandler',
            'stream': sys.stdout,
            'formatter': 'general',
        },
        'console': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        '': {
            'level': env.str(var='EXCEPTION_LOG_LEVEL', default='WARNING'),
            'handlers': ['file_exceptions'],
            'propagate': True,
        },
        'django.db.backends': {  # log sql queries
            'level': env.str(var='DJANGO_LOG_LEVEL', default='ERROR'),
            'handlers': ['console'],
        },
    },
}

# DRF
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': ('rest_framework_simplejwt.authentication.JWTAuthentication',),
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
    ),
    'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.AllowAny',),
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    # Generic view settings
    'SEARCH_PARAM': 'search',
    'ORDERING_PARAM': 'order',
    # Pagination settings
    'PAGE_SIZE': 10,
    'DEFAULT_PAGINATION_CLASS': 'core.pagination.PageNumberPagination',
    'MAXIMUM_PAGE_SIZE': 100,
    # Version settings
    # 'DEFAULT_VERSION': None,
    # 'ALLOWED_VERSIONS': None,
    # 'VERSION_PARAM': 'v',
    # 'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.AcceptHeaderVersioning',
    # Date and Time
    'DATE_FORMAT': 'iso-8601',
    'TIME_FORMAT': 'iso-8601',
    'DATETIME_FORMAT': 'iso-8601',
    # 'DATETIME_FORMAT': "%Y-%m-%d - %H:%M:%S",
    # Encoding
    'COMPACT_JSON': True,
    # Miscellaneous settings
    'EXCEPTION_HANDLER': 'core.handlers.exception_handler',
    'NON_FIELD_ERRORS_KEY': 'non_field_errors',
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=5),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': False,
    'UPDATE_LAST_LOGIN': False,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,
    'JSON_ENCODER': None,
    'JWK_URL': None,
    'LEEWAY': 0,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'id',
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'TOKEN_USER_CLASS': 'rest_framework_simplejwt.models.TokenUser',
    'JTI_CLAIM': 'jti',
    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
    'TOKEN_OBTAIN_SERIALIZER': 'rest_framework_simplejwt.serializers.TokenObtainPairSerializer',
    'TOKEN_REFRESH_SERIALIZER': 'rest_framework_simplejwt.serializers.TokenRefreshSerializer',
    'TOKEN_VERIFY_SERIALIZER': 'rest_framework_simplejwt.serializers.TokenVerifySerializer',
    'TOKEN_BLACKLIST_SERIALIZER': 'rest_framework_simplejwt.serializers.TokenBlacklistSerializer',
    'SLIDING_TOKEN_OBTAIN_SERIALIZER': 'rest_framework_simplejwt.serializers.TokenObtainSlidingSerializer',
    'SLIDING_TOKEN_REFRESH_SERIALIZER': 'rest_framework_simplejwt.serializers.TokenRefreshSlidingSerializer',
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'Formaloo API',
    'DESCRIPTION': 'Formaloo API documentation',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'SERVE_PUBLIC': True,
    'DEFAULT_GENERATOR_CLASS': 'drf_spectacular.generators.SchemaGenerator',
    'COMPONENT_SPLIT_PATCH': True,
    'COMPONENT_SPLIT_REQUEST': True,
    'SERVE_PERMISSIONS': ['core.permissions.IsSuperUser'],
    'SERVE_AUTHENTICATION': ['rest_framework.authentication.BasicAuthentication'],
    'SWAGGER_UI_OAUTH2_CONFIG': {},
    'SWAGGER_UI_SETTINGS': {
        'deepLinking': True,
        'displayRequestDuration': True,
        'requestSnippetsEnabled': True,
        'syntaxHighlight': True,
    },
    'REDOC_UI_SETTINGS': {},
    'POSTPROCESSING_HOOKS': ['drf_spectacular.hooks.postprocess_schema_enums'],
    'SORT_OPERATIONS': True,
    'GET_MOCK_REQUEST': 'drf_spectacular.plumbing.build_mock_request',
    'DISABLE_ERRORS_AND_WARNINGS': False,
    'SCHEMA_PATH_PREFIX': None,
    'SCHEMA_PATH_PREFIX_TRIM': False,
    'SCHEMA_PATH_PREFIX_INSERT': '',
    'SCHEMA_COERCE_PATH_PK_SUFFIX': False,
    'SERVE_URLCONF': None,
    'SWAGGER_UI_DIST': 'https://cdn.jsdelivr.net/npm/swagger-ui-dist@latest',
    'SWAGGER_UI_FAVICON_HREF': 'https://cdn.jsdelivr.net/npm/swagger-ui-dist@latest/favicon-32x32.png',
    'REDOC_DIST': 'https://cdn.jsdelivr.net/npm/redoc@latest',
    'CONTACT': {},
    'LICENSE': {},
    'EXTERNAL_DOCS': {},
    'EXTENSIONS_INFO': {},
    'EXTENSIONS_ROOT': {},
    'OAUTH2_FLOWS': [],
    'OAUTH2_AUTHORIZATION_URL': None,
    'OAUTH2_TOKEN_URL': None,
    'OAUTH2_REFRESH_URL': None,
    'OAUTH2_SCOPES': None,
}

# Cache
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': env.str(var='DEFAULT_REDIS_URL', default='redis://redis:6379/0'),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'SOCKET_CONNECT_TIMEOUT': 5,
            'SOCKET_TIMEOUT': 5,
        },
    },
}
