"""
Django settings for ITShowPlatform project.

Generated by 'django-admin startproject' using Django 4.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

from pathlib import Path
import os
import configparser

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

conf = configparser.RawConfigParser()

conf.read(os.path.join(BASE_DIR, "config.ini"), encoding="utf-8")

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = conf.get("Django", "SECRET_KEY"),

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]

# Application definition



INSTALLED_APPS = [
    'simpleui',
    'corsheaders',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'apps.enroll',
    'apps.history',
    'apps.comments',
    'apps.work',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
]

ROOT_URLCONF = 'ITShowPlatform.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
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

WSGI_APPLICATION = 'ITShowPlatform.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
     'default': {
        'ENGINE': conf.get("database","ENGINE"),
        'NAME': conf.get("database","NAME"),
        'USER': conf.get("database","USER"),
        'PASSWORD': conf.get("database","PASSWORD"),
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'zh-Hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (  # ?????????????????????
        'rest_framework.renderers.JSONRenderer',  # json?????????
        'rest_framework.renderers.BrowsableAPIRenderer',  # ??????API?????????
    )
}

EMAIL_HOST = conf.get('email',"EMAIL_HOST")  # ?????????
EMAIL_PORT = conf.get("email","EMAIL_PORT")
EMAIL_HOST_USER = conf.get("email","EMAIL_HOST_USER")  # ??????
EMAIL_HOST_PASSWORD = conf.get("email","EMAIL_HOST_PASSWORD")  # ?????? (??????????????????????????????????????????)
EMAIL_USE_SSL = conf.get("email","EMAIL_USE_SSL")  # ????????????False
EMAIL_FROM = conf.get("email","EMAIL_FROM")  # ????????????

SIMPLEUI_HOME_INFO = False
SIMPLEUI_ANALYSIS = False

ADMINS = (
    ('ladeng', '2312936963@qq.com'),
)
MANAGERS = ADMINS

# ??????log??????????????????
LOG_DIR = os.path.join(BASE_DIR, "logs")
if not os.path.exists(LOG_DIR):
    os.mkdir(LOG_DIR)

# ??????????????????????????????
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,  # ?????????????????????logger??????
    "filters": {"require_debug_false": {"()": "django.utils.log.RequireDebugFalse"}},
    "formatters": {  # ???????????????????????????
        "verbose": {  # ??????
            "format": "%(levelname)s %(asctime)s %(module)s "
                      "%(process)d %(thread)d %(message)s"
        },
        'simple': {  # ??????
            'format': '[%(levelname)s][%(asctime)s][%(filename)s:%(lineno)d]%(message)s'
        },
    },
    "handlers": {  # ?????????????????????????????????
        "mail_admins": {  # ??????debug=False???Error????????????????????????admin
            "level": "ERROR",
            "filters": ["require_debug_false"],
            "class": "django.utils.log.AdminEmailHandler",
        },
        'file': {  # ???INFO?????????????????????????????????????????????
            'level': "INFO",
            'class': 'logging.handlers.RotatingFileHandler',  # ???????????????????????????
            'filename': os.path.join(LOG_DIR, 'django.log'),  # ???????????????
            'maxBytes': 1024 * 1024 * 10,  # ???????????????????????????10M
            'backupCount': 5,  # ??????????????????????????????
            'formatter': 'simple',  # ????????????
            'encoding': 'utf-8',  # ??????????????????
        },
        "console": {  # ???????????????console
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "root": {"level": "INFO", "handlers": ["console"]},
    "loggers": {
        "django.request": {  # Django???request??????error???????????????
            "handlers": ["mail_admins"],
            "level": "ERROR",
            "propagate": True,  # ????????????????????????logger??????
        },
        "django.security.DisallowedHost": {  # ???????????? ALLOWED_HOSTS ?????????????????????????????????
            "level": "ERROR",
            "handlers": ["console", "mail_admins"],
            "propagate": True,
        },
    },
}

CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_ALLOW_ALL = True
CORS_ORIGIN_WHITELIST = (
    ['http://127.0.0.1:*']
)
CORS_ALLOW_METHODS = (
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
    'VIEW',
)



CORS_ALLOW_HEADERS = (
    'XMLHttpRequest',
    'X_FILENAME',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
    'Pragma',
)
