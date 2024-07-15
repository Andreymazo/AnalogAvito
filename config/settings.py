import os
from pathlib import Path
from datetime import timedelta
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
BASE_URL = os.getenv("BASE_URL")

env_path = BASE_DIR / ".env"
load_dotenv(dotenv_path=env_path)

SECRET_KEY = os.getenv("SECRET_KEY")

DEBUG = True

ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [
    "modeltranslation",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.gis",
    "django.contrib.sites",
    "debug_toolbar",
    "rest_framework",
    'rest_framework_gis',
    "mptt",
    "ad.apps.AdConfig",
    "bulletin.apps.BulletinConfig",
    "users.apps.UsersConfig",
    "drf_spectacular",
    'django_filters',
    "map",
    
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django_session_timeout.middleware.SessionTimeoutMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    
]

INTERNAL_IPS = [
    # ...
    "127.0.0.1",
    # ...
]
# TESTING = "test" in sys.argv

# if not TESTING:
#     INSTALLED_APPS = [
#         *INSTALLED_APPS,
#         "debug_toolbar",
#     ]
#     MIDDLEWARE = [
#         "debug_toolbar.middleware.DebugToolbarMiddleware",
#         *MIDDLEWARE,
#     ]

SPECTACULAR_SETTINGS = {
    "TITLE": "Bulletin board",
    "DESCRIPTION": "Django5 Test Swagger API description",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    # OTHER SETTINGS,
    "COMPONENT_SPLIT_REQUEST": True
}

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, 'bulletin/templates/'), BASE_DIR],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                'django.template.context_processors.i18n',
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

DATABASES = {
    "default": {
        # "ENGINE": "django.db.backends.postgresql",
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        "NAME": os.getenv("DB_NAME"),
        "HOST": os.getenv("DB_HOST"),
        "PORT": os.getenv("DB_PORT"),
        "USER": os.getenv("DB_USER"),
        "PASSWORD": os.getenv("DB_PASSWORD"),
    }
}

AUTH_USER_MODEL = "users.CustomUser"

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation"
                ".UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation"
                ".MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation"
                ".CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation"
                ".NumericPasswordValidator",
    },
]

LANGUAGE_CODE = "ru"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


gettext = lambda s: s
LANGUAGES = (
    ("es", gettext("Spanish")),
    ("ru", gettext("Russia")),
    ("en", gettext("English")),
    
)

LOCALE_PATHS = (
    os.path.join(BASE_DIR, "locale"),
)

MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"

# STATICFILES_DIRS = [ os.path.join(BASE_DIR, "static"), ]

STATIC_URL = "static/"
# STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATICFILES_DIRS = (os.path.join(BASE_DIR, "static"),)

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = os.getenv("EMAIL_PORT")
EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS", "False") == "True"
EMAIL_USE_SSL = os.getenv("EMAIL_USE_SSL", "True") == "True"

EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL")


# SESSION_COOKIE_DOMAIN = None
# SESSION_COOKIE_SECURE = False
# SESSION_COOKIE_AGE = 10  # 30 minutes. "1209600(2 weeks)" by default
# SESSION_SAVE_EVERY_REQUEST = True  # "False" by default
SESSION_EXPIRE_SECONDS = 1800  # Expire after 30 minutes
SESSION_EXPIRE_AFTER_LAST_ACTIVITY = True
SESSION_TIMEOUT_REDIRECT = "bulletin:sign_in_email"  # Add your URL
SESSION_EXPIRE_AT_BROWSER_CLOSE = True  # Invalid session

ATTEMPTS = 3  # Максимальное количество попыток ввести код
SITE_ID = 1

REST_FRAMEWORK = {

    # 'DEFAULT_PARSER_CLASSES': [
    #     # 'rest_framework.parsers.JSONParser',
    #     'rest_framework.parsers.FormParser',
    #     'rest_framework.parsers.MultiPartParser',
    #     'rest_framework.parsers.FileUploadParser'
    # ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        
        # "rest_framework.authentication.BasicAuthentication'",
        "rest_framework.authentication.SessionAuthentication",
        # "rest_framework.authentication.TokenAuthentication"
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    'DEFAULT_FILTER_BACKENDS':(
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.OrderingFilter', 
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 5,

#     'FILE_UPLOAD_HANDLERS' : [
    
#     "django.core.files.uploadhandler.MemoryFileUploadHandler",
#     "django.core.files.uploadhandler.TemporaryFileUploadHandler",
# ]
}
# SERIALIZATION_MODULES = {
#     "geojson": "django.contrib.gis.serializers.geojson",
#  }
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": False,
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_USER_CLASS": "rest_framework_simplejwt.models.TokenUser",
    "AUTH_HEADER_TYPES": ("Bearer",),
}


DATA_UPLOAD_MAX_MEMORY_SIZE = 5242880
SESSION_EXPIRE_SECONDS = 30 * 60  # Expire after 30 minutes
SESSION_EXPIRE_AFTER_LAST_ACTIVITY = True
# SESSION_TIMEOUT_REDIRECT = "bulletin:log_in"  # Add your URL
SESSION_EXPIRE_AT_BROWSER_CLOSE = True  # Invalid session
