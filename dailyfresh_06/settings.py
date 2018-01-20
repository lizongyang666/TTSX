"""
Django settings for daliyfresh_06 project.

Generated by 'django-admin startproject' using Django 1.8.7.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

# from django.conf.global_settings import STATICFILES_DIRS, DATABASE_ROUTERS, AUTH_USER_MODEL

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# 添加app应用所在路径到python解释的导包路径中
import sys
sys.path.insert(1, os.path.join(BASE_DIR, 'apps'))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'cy9k&sv4+oct)5tk9audj@gan0_8k8lgkc!5vnu5f61qwh74*5'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'tinymce', # 富文本编辑器
    'users',
    'goods',
    'orders',
    'carts',
)

# 声明django自带的认证系统要使用的用户数据表对应的模型类
# AUTH_USER_MODEL = '应用名.模型类名'
AUTH_USER_MODEL = 'users.User'

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'dailyfresh_06.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "templates")],
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

WSGI_APPLICATION = 'dailyfresh_06.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': '192.168.162.130',
        'PORT': 3306,
        'NAME': 'dailyfresh_06',
        'USER': 'root',
        'PASSWORD': 'mysql',
    },

    'slave': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': '192.168.162.130',
        'PORT': 3306,
        'NAME': 'dailyfresh_06',
        'USER': 'root',
        'PASSWORD': 'mysql',
    }
}

# 指明数据库的读写分离路由
DATABASE_ROUTERS = ['utils.db_routers.MasterSlaveRouter']


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

# Email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.qq.com'
EMAIL_PORT = 465
EMAIL_HOST_USER = 'aleoyang@foxmail.com'
EMAIL_HOST_PASSWORD = 'dwlavyrbahlmcajg'
EMAIL_FROM = '天天生鲜<aleoyang@foxmail.com>'


CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://192.168.162.130',
        'OPTIONS':{
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'default'

# 被django的login_required装饰使用的参数，登录的网页网址
LOGIN_URL = 'users/login'

# FastDFS客户段的配置文件路径
FASTDFS_CLIENT_CONF = os.path.join(BASE_DIR, 'utils/fastdfs_storage/client.conf')

FASTDFS_NGINX_URL = 'HTTP://192.168.162.130/'

# 指明django使用的默认文件存储系统
DEFAULT_FILE_STORAGE = 'utils.fastdfs_storage.storage.FastDFSStorage'

# tinymce 富文本编辑器的配置参数
TINYMCE_DEFAULT_CONFIG = {
    'theme': 'advanced',
    'width': 600,
    'height': 400,
}