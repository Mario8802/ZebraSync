"""
Django settings for zebrasync project (production-ready with Google login).
"""

import dj_database_url
from pathlib import Path
import os
from dotenv import load_dotenv

# =============================================================================
# Base Directory & Environment
# =============================================================================
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

# =============================================================================
# Core Security Settings
# =============================================================================
SECRET_KEY = os.getenv("SECRET_KEY", "!!!change-me-in-prod!!!")
DEBUG = os.getenv("DEBUG", "False").lower() in ("true", "1", "yes")

RENDER_HOST = os.getenv("RENDER_EXTERNAL_HOSTNAME")

ALLOWED_HOSTS = [
    "zebrasync.onrender.com",
]

CSRF_TRUSTED_ORIGINS = [
    "https://zebrasync.onrender.com",
]
# =============================================================================
# Application Definition
# =============================================================================
INSTALLED_APPS = [
    # Django core
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",

    # Third-party
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",

    # Local apps
    "core",
]

SITE_ID = 1

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "allauth.account.middleware.AccountMiddleware",

]

ROOT_URLCONF = "zebrasync.urls"
WSGI_APPLICATION = "zebrasync.wsgi.application"

# =============================================================================
# Templates Configuration
# =============================================================================
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",  # Required by allauth
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",

            ],
        },
    },
]

# =============================================================================
# Database Configuration
# =============================================================================
DATABASES = {
    "default": dj_database_url.config(
        conn_max_age=600,
        ssl_require=True
    )
}

# =============================================================================
# Authentication & Allauth
# =============================================================================
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]

LOGIN_REDIRECT_URL = "/dashboard/"
ACCOUNT_LOGOUT_REDIRECT_URL = "/"
ACCOUNT_LOGIN_METHODS = {"username", "email"}
ACCOUNT_SIGNUP_FIELDS = ["email*", "username*", "password1*", "password2*"]
ACCOUNT_EMAIL_VERIFICATION = "none"

SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "APP": {
            "client_id": os.getenv("SOCIALACCOUNT_GOOGLE_CLIENT_ID"),
            "secret": os.getenv("SOCIALACCOUNT_GOOGLE_SECRET"),
            "key": "",
        },
        "SCOPE": ["profile", "email"],
        "AUTH_PARAMS": {"access_type": "online"},
        "OAUTH_PKCE_ENABLED": True,
    }
}




# =============================================================================
# Static & Media Files
# =============================================================================
STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# =============================================================================
# Celery Configuration
# =============================================================================
CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")
CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", CELERY_BROKER_URL)

# =============================================================================
# Internationalization
# =============================================================================
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# =============================================================================
# Miscellaneous
# =============================================================================
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LOGGING = {
    "version": 1,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "WARNING",
    },
}

