"""
Django settings for mr_chat project.

Generated by 'django-admin startproject' using Django 5.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
import os
from decouple import  config
import dj_database_url
from dotenv import load_dotenv


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent



STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']  # Ensure your static folder is listed
STATIC_ROOT = BASE_DIR / 'staticfiles'  # Specify a directory for collected files

# Whitenoise settings
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/images/'
MEDIA_ROOT = BASE_DIR / 'images'

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/login/'

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# / SECURITY /#
# SECURE_SSL_REDIRECT = True
# SECURE_BROWSER_XSS_FILTER = True
# SECURE_CONTENT_TYPE_NOSNIFF = True
# SECURE_HSTS_SECONDS = 86400
# SECURE_HSTS_PRELOAD = True
# SECURE_HSTS_INCLUDE_SUBDOMAINS = True
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True


CSP_DEFAULT_SRC = ["'self'"]
CSP_CONNECT_SRC = ["'self'", "wss://mr-chat.onrender.com", "ws://mr-chat.onrender.com"]



# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')


DEBUG = config("DEBUG", cast=bool)

if DEBUG is False:
    STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

# WebSocket URL for Django Channels
WS_PROTOCOL = 'wss' if not DEBUG else 'ws'



DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': lambda request: DEBUG,


}








ALLOWED_HOSTS = ['https://mr-chat.onrender.com','localhost','*']

load_dotenv()

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = config('EMAIL_HOST')  # Get the email host from the .env file
EMAIL_PORT =  config('EMAIL_PORT')# Default to 587 if not set in .env
EMAIL_USE_TLS = config('EMAIL_USE_TLS') == "True"  # Convert to boolean
EMAIL_HOST_USER = config('EMAIL_HOST_USER') # Your email username from .env
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')# Your email password from .env
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL')  # Default sender email




ENVIRONMENT = 'development'

if ENVIRONMENT == 'development':
    CHANNEL_LAYERS = {
        "default": {
            "BACKEND": "channels.layers.InMemoryChannelLayer"
        }
    }
else:
    redis_url = os.getenv('REDIS_URL')
    if not redis_url:
        raise ValueError("REDIS_URL environment variable is not set in production mode")

    CHANNEL_LAYERS = {
        "default": {
            "BACKEND": "channels.layers.InMemoryChannelLayer",
            "CONFIG": {
                "hosts": [(redis_url)],
            }
        }
    }

# Application definition

INSTALLED_APPS = [
    "unfold",  # before django.contrib.admin
    "unfold.contrib.filters",  # optional, if special filters are needed
    "unfold.contrib.forms",  # optional, if special form elements are needed
    "unfold.contrib.inlines",  # optional, if special inlines are needed
    "unfold.contrib.import_export",  # optional, if django-import-export package is used
    "unfold.contrib.guardian",  # optional, if django-guardian package is used
    "unfold.contrib.simple_history",
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.admin.options',
    'uvicorn',
    "daphne",
    'mr_chat',
    'django.contrib.staticfiles',
    'mr_chat.profiles',
    'mr_chat.chat_app',
    "channels",
    'csp',
    'gunicorn',
]


ASGI_APPLICATION = 'mr_chat.asgi.application'

CSRF_TRUSTED_ORIGINS = ['https://mr-chat.onrender.com']




MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'mr_chat.chat_app.middleware.CookieMiddleware',
    'csp.middleware.CSPMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.gzip.GZipMiddleware',

]








ROOT_URLCONF = 'mr_chat.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
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

WSGI_APPLICATION = 'mr_chat.wsgi.application'




# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases



SESSION_ENGINE = 'django.contrib.sessions.backends.cache'

DATABASES = {
    'default': {
        'ENGINE': os.getenv('DB_ENGINE'),
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
    }
}

DATABASES["default"] = dj_database_url.parse('postgresql://mr_chat_21tp_user:KD1cv3BzWi9SFTAtP8YN5dsmsSrEVsqa@dpg-ct7ls3ogph6c73cfhl80-a.oregon-postgres.render.com/mr_chat_21tp')

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True



DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'



