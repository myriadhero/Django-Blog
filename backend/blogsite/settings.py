"""
Django settings for blogsite project.

Generated by 'django-admin startproject' using Django 4.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get("DJANGO_DEBUG").lower() in ("true", "1", "t")

if not DEBUG:
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_SECURE = True
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS").split(",") or [
    "localhost",
    "127.0.0.1",
]

if DEBUG:
    INTERNAL_IPS = [
        "localhost",
        "127.0.0.1",
    ]

SITE_ID = 1

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "django.contrib.sitemaps",
    "django.contrib.postgres",
    "ckeditor",
    "ckeditor_uploader",
    "fontawesomefree",
    "django_select2",
    "crispy_forms",
    "crispy_bulma",
    "core.apps.CoreConfig",
    "blog.apps.BlogConfig",
]
if DEBUG:
    INSTALLED_APPS.append("debug_toolbar")

    import mimetypes

    mimetypes.add_type("application/javascript", ".js", True)

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]
if DEBUG:
    MIDDLEWARE.insert(3, "debug_toolbar.middleware.DebugToolbarMiddleware")

ROOT_URLCONF = "blogsite.urls"

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

WSGI_APPLICATION = "blogsite.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "HOST": os.environ.get("POSTGRES_DB_HOST"),
        "PORT": os.environ.get("POSTGRES_DB_PORT", 5432),
        "NAME": os.environ.get("POSTGRES_DB_NAME"),
        "USER": os.environ.get("POSTGRES_DB_USER"),
        "PASSWORD": os.environ.get("POSTGRES_DB_PASSWORD"),
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "en-us"
TIME_ZONE = os.environ.get("DJANGO_TIME_ZONE")
USE_I18N = False
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATICFILES_STORAGE = "django.contrib.staticfiles.storage.ManifestStaticFilesStorage"
STATIC_URL = "static/"
STATIC_ROOT = os.environ.get("STATICFILES_DIR") or BASE_DIR / "staticfiles"

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"


TAGGIT_CASE_INSENSITIVE = True
TAGGIT_TAGS_FROM_STRING = "blog.utils.utils.comma_splitter"
TAGGIT_STRING_FROM_TAGS = "blog.utils.utils.comma_joiner"


CKEDITOR_CONFIGS = {
    "default": {
        "toolbar_Custom": [
            {
                "name": "document",
                "items": [
                    "Source",
                ],
            },
            {"name": "editing", "items": ["Find", "Replace", "-", "SelectAll"]},
            {
                "name": "tools",
                "items": [
                    "Maximize",
                    "ShowBlocks",
                    "Preview",
                ],
            },
            "/",  # put this to force next toolbar on new line
            {"name": "styles", "items": ["Styles", "Format", "Font", "FontSize"]},
            {
                "name": "basicstyles",
                "items": [
                    "Bold",
                    "Italic",
                    "Underline",
                    "Strike",
                    "Subscript",
                    "Superscript",
                    "-",
                    "RemoveFormat",
                ],
            },
            "/",  # put this to force next toolbar on new line
            {
                "name": "paragraph",
                "items": [
                    "NumberedList",
                    "BulletedList",
                    "-",
                    "Outdent",
                    "Indent",
                    "-",
                    "Blockquote",
                    "CreateDiv",
                    "-",
                    "JustifyLeft",
                    "JustifyCenter",
                    "JustifyRight",
                    "JustifyBlock",
                ],
            },
            {"name": "colors", "items": ["TextColor", "BGColor"]},
            {"name": "links", "items": ["Link", "Unlink", "Anchor"]},
            "/",  # put this to force next toolbar on new line
            {
                "name": "insert",
                "items": [
                    "Image",
                    "Flash",
                    "Table",
                    "HorizontalRule",
                    "Smiley",
                    "SpecialChar",
                ],
            },
        ],
        "toolbar": "Custom",
        "tabSpaces": 4,
        "extraPlugins": ",".join(
            [
                "uploadimage",  # the upload image feature
                "image",
                "filebrowser",
                "autolink",
                "autogrow",
            ]
        ),
        "filebrowserUploadUrl": "/ckeditor/upload/",
        "extraAllowedContent": "blockquote(twitter-tweet)[data-conversation]; p[lang,dir]",
    },
}

CKEDITOR_UPLOAD_PATH = "uploads/"
CKEDITOR_IMAGE_BACKEND = "pillow"
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"


CRISPY_ALLOWED_TEMPLATE_PACKS = ("bulma",)
CRISPY_TEMPLATE_PACK = "bulma"

# it is recommended to change django admin url path from the default admin/
ADMIN_PATH = os.environ.get("DJANGO_ADMIN_PATH") or "admin/"

LOGS_DIR = os.environ.get("LOGS_DIR", BASE_DIR / "logs")

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
        "file": {
            "level": "INFO",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": os.path.join(LOGS_DIR, "django.log"),
            "maxBytes": 1024 * 1024 * 5,  # 5MB
            "backupCount": 5,  # 5 total files
            # "formatter": "verbose",
        },
    },
    "root": {
        "handlers": ["file"],
        "level": "INFO",
    },
}
