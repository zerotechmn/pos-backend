"""
Django settings for backend project.

Generated by 'django-admin startproject' using Django 5.2.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.2/ref/settings/
"""

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure--kk!dw&u($^eq!1+8sziay7)mr-q-xzo01ep@)i^6c&u2w$9z='

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'oauth2_provider',
    'backend.base.apps.BaseConfig',
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

ROOT_URLCONF = 'backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'backend.wsgi.application'

OAUTH2_PROVIDER = {
    "ACCESS_TOKEN_EXPIRE_SECONDS": 3600,  # Access токены хугацаа (1 цаг)
    "AUTHORIZATION_CODE_EXPIRE_SECONDS": 300,  # Authorization code-ийн хугацаа (5 минут)
    "REFRESH_TOKEN_EXPIRE_SECONDS": 86400,  # Refresh токены хугацаа (1 өдөр)
    "SCOPES": {
        "read": "Read access",
        "write": "Write access",
    },
    "ROTATE_REFRESH_TOKEN": True,  # refresh token солигддог байх эсэх
    "OAUTH2_BACKEND_CLASS": "oauth2_provider.oauth2_backends.OAuthLibCore",  # default backend
    "RESOURCE_SERVER_INTROSPECTION_URL": "https://provider.com/o/introspect/",
    "RESOURCE_SERVER_INTROSPECTION_CREDENTIALS": ("client_id", "client_secret"),
}

AUTH_USER_MODEL = 'base.User'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication'
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
}

# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'OPTIONS': {
            'options': '-c search_path=django,public',
        },
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME', 'zerotech'),
        'USER': os.environ.get('DB_USER', 'zerotech'),
        'PASSWORD': os.environ.get('DB_PASSWORD', 'postgres'),
        'HOST': os.environ.get('DB_HOST', '192.168.1.38'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


INSTALLED_APPS += ['corsheaders']
MIDDLEWARE = ['corsheaders.middleware.CorsMiddleware'] + MIDDLEWARE
CORS_ALLOW_ALL_ORIGINS = True


API_EBARIMT_URL = "http://api.ebarimt.mn"
B2B_URL = "https://b2b-indol.vercel.app"
B2C_URL = "https://orange-api.shunkhlai.mn"
EBARIMT_30_URL = "http://103.168.179.44:3000"
EBARIMT_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJlNzkxMjNjOS02MjU3LTQ2OTEtOWVmOS04MDE2MTExNGYzOTYiLCJuYW1lIjoiT25saW5lIFBPUyIsImF1ZCI6InBvcyIsImlhdCI6MTc0NTMwOTAwOCwiZXhwIjoyNzQ1MzEyNjA4fQ.OcrZMlAR1DdJXjfuFTF89mM0VUBBOKGFd9_wL-1UQIw"
EBARIMT_URL = "http://oes.shunkhlai.mn:8011"
LOYALTY_URL = "https://lms.shunkhlai.mn"
MERCHANT_URL = "http://info.ebarimt.mn"
GUUR_URL = "http://testsvr.shunkhlai.mn:8073"
VERSION_URL = "http://192.168.1.165:9000/update_info.json"

# Discord Server URL
DISCORD_EBARIMT_CHANNEL_URL = ""
DISCORD_SET_TERMINAL_CHANNEL_URL = ""

# Teams Server URL
TEAMS_CHANNEL_URL = ""