from pathlib import Path
from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).parents[2]
APPS_DIR = BASE_DIR / "backend" / "project"


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config("DEBUG", default=False, cast=bool)

ALLOWED_HOSTS = []


# Application definition

DJANGO_APPS = [
    # General use templates & template tags (should appear first)
    # 'adminlte3',
    # Optional: Django admin theme (must be before django.contrib.admin)
    # 'adminlte3_theme',
    "django.contrib.admin",
    "django.contrib.auth",
    "django_email_verification",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # For Fuzzy Search
    "django.contrib.postgres",
    "rest_framework",
    "rest_framework.authtoken",
]


THIRD_PARTY_APPS = [
    "softdelete",
    "generic_relations",
    "rest_framework_recaptcha",
]

PROJECT_APPS = [
    "project.users",
    "project.notifications",
    "project.reports",
    "project.teams",
    "project.conversations",
    "project.posts",
    "project.help",
    "project.administration",
    "project.custom_services",
    "project.single_page",
]

INSTALLED_APPS = DJANGO_APPS + PROJECT_APPS + THIRD_PARTY_APPS

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"
TEMPLATE_PATH = BASE_DIR.joinpath("winoutt-django/backend/project/templates")
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [TEMPLATE_PATH],
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

WSGI_APPLICATION = "config.wsgi.application"


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": config("DB_ENGINE", default="django.db.backends.sqlite3"),
        "NAME": config("DB_NAME", default=[BASE_DIR.joinpath("db.sqlite3")]),
        "USER": config("DB_USER", default=""),
        "PASSWORD": config("DB_PASSWORD", default=""),
        "HOST": config("DB_HOST", default=""),
        "PORT": config("DB_PORT", default=""),
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = [
    BASE_DIR.joinpath("public")
]  # after collect static is run all the static files will be put in this folder


# To use knox as authentication classes
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 20,
}

# To stop Django from checking in_active users, Only write this if want to handle in_active users manually through code
AUTHENTICATION_BACKENDS = ["django.contrib.auth.backends.AllowAllUsersModelBackend"]

# For password reset
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# For Email Confirmation
EMAIL_ACTIVE_FIELD = config("EMAIL_ACTIVE_FIELD", default="is_active")
EMAIL_SERVER = config("EMAIL_SERVER", default="smtp.gmail.com")
EMAIL_PORT = config("EMAIL_PORT", cast=int, default=587)
EMAIL_ADDRESS = config("EMAIL_ADDRESS", default="")
EMAIL_FROM_ADDRESS = config("EMAIL_FROM_ADDRESS", default="")
EMAIL_PASSWORD = config("EMAIL_PASSWORD", default="")
EMAIL_MAIL_SUBJECT = config("EMAIL_MAIL_SUBJECT", default="Confirm your email")
EMAIL_MAIL_HTML = config("EMAIL_MAIL_HTML", default="")
EMAIL_MAIL_PLAIN = config("EMAIL_MAIL_PLAIN", default="")
EMAIL_PAGE_TEMPLATE = config("EMAIL_PAGE_TEMPLATE", default="")
EMAIL_PAGE_DOMAIN = config("EMAIL_PAGE_DOMAIN", default="http://localhost:8000/")

# To send custom msg emails

EMAIL_HOST = config("EMAIL_HOST", default="")
EMAIL_HOST_USER = config("EMAIL_HOST_USER", default="")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD", default="")
EMAIL_PORT = config("EMAIL_PORT", default=587, cast=int)
EMAIL_USE_TLS = config("EMAIL_USE_TLS", default=True, cast=bool)


PUSHER_APP_ID = config("PUSHER_APP_ID", default="")
PUSHER_APP_KEY = config("PUSHER_APP_KEY", default="")
PUSHER_SECRET = config("PUSHER_SECRET", default="")
PUSHER_CLUSTER = config("PUSHER_CLUSTER", default="")


# Google Recaptcha Keys
DRF_RECAPTCHA_SECRET_KEY = config("RECAPTCHA_PRIVATE_KEY", default="")
