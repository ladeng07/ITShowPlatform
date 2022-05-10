from pathlib import Path
import os
import configparser
import logging

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
    'corsheaders',
    'simpleui',
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
    # 'django.middleware.csrf.CsrfViewMiddleware',
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
        'ENGINE': conf.get("database", "ENGINE"),
        'NAME': conf.get("database", "NAME"),
        'USER': conf.get("database", "USER"),
        'PASSWORD': conf.get("database", "PASSWORD"),
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
    'DEFAULT_RENDERER_CLASSES': (  # 默认响应渲染类
        'rest_framework.renderers.JSONRenderer',  # json渲染器
        'rest_framework.renderers.BrowsableAPIRenderer',  # 浏览API渲染器
    )
}

EMAIL_HOST = conf.get('email', "EMAIL_HOST")  # 服务器
EMAIL_PORT = int(conf.get("email", "EMAIL_PORT"))
EMAIL_HOST_USER = conf.get("email", "EMAIL_HOST_USER")  # 账号
EMAIL_HOST_PASSWORD = conf.get("email", "EMAIL_HOST_PASSWORD")  # 密码 (注意：这里的密码指的是授权码)
EMAIL_USE_SSL = bool(conf.get("email", "EMAIL_USE_SSL"))  # 一般都为False
EMAIL_FROM = conf.get("email", "EMAIL_FROM")  # 邮箱来自

print(conf.get('email', "EMAIL_HOST"), conf.get("email", "EMAIL_PORT"), conf.get("email", "EMAIL_HOST_USER"),
      conf.get("email", "EMAIL_HOST_PASSWORD"))
ADMINS = (
    ('ladeng', '2312936963@qq.com'),
)
MANAGERS = ADMINS

# 创建log文件的文件夹
LOG_DIR = os.path.join(BASE_DIR, "logs")
if not os.path.exists(LOG_DIR):
    os.mkdir(LOG_DIR)

# 基本配置，可以复用的
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,  # 禁用已经存在的logger实例
    "filters": {"require_debug_false": {"()": "django.utils.log.RequireDebugFalse"}},
    "formatters": {  # 定义了两种日志格式
        "verbose": {  # 详细
            "format": "%(levelname)s %(asctime)s %(module)s "
                      "%(process)d %(thread)d %(message)s"
        },
        'simple': {  # 简单
            'format': '[%(levelname)s][%(asctime)s][%(filename)s:%(lineno)d]%(message)s'
        },
    },
    "handlers": {  # 定义了三种日志处理方式
        "mail_admins": {  # 只有debug=False且Error级别以上发邮件给admin
            "level": "ERROR",
            "filters": ["require_debug_false"],
            "class": "django.utils.log.AdminEmailHandler",
        },
        'file': {  # 对INFO级别以上信息以日志文件形式保存
            'level': "INFO",
            'class': 'logging.handlers.RotatingFileHandler',  # 滚动生成日志，切割
            'filename': os.path.join(LOG_DIR, 'django.log'),  # 日志文件名
            'maxBytes': 1024 * 1024 * 10,  # 单个日志文件最大为10M
            'backupCount': 5,  # 日志备份文件最大数量
            'formatter': 'simple',  # 简单格式
            'encoding': 'utf-8',  # 放置中文乱码
        },
        "console": {  # 打印到终端console
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "root": {"level": "INFO", "handlers": ["console"]},
    "loggers": {
        "django.request": {  # Django的request发生error会自动记录
            "handlers": ["mail_admins"],
            "level": "ERROR",
            "propagate": True,  # 向不向更高级别的logger传递
        },
        "django.security.DisallowedHost": {  # 对于不在 ALLOWED_HOSTS 中的请求不发送报错邮件
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
