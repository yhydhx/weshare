
# coding:utf-8

"""
Django settings for gt project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'j=u@d8)c6vpmjf-*=6y8&9k#1n+d66py(blo0!$@l+qfcvt+9@'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 'game',
    'frontEnd',

    'backEnd',
    'payment',
    'api'

)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'gt.urls'

WSGI_APPLICATION = 'gt.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django_mongodb_engine',
        'NAME': "weshare",
        # 'USER': 'jupiter',
        # 'PASSWORD' : '5080',
        'HOST': '120.24.156.181',
        # 'HOST': '127.0.0.1',

        'PORT': '27017',
    }
}

#用户状态
HOST_STATE = {
    'GUEST' : 0,
    'APPLY' : 1,
    'HOST'  : 2,
}

#订单的状态
BILL_STATE = {
    'INIT' : 0,
}


# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = BASE_DIR + "/gt/static/"
UPLOAD_PATH = STATIC_ROOT + "upload/"

STATICfILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
    '/var/www/html/gt/gt/static'
)

# email setting
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.mxhichina.com'
EMAIL_PORT = 25
EMAIL_HOST_USER = 'service@wshere.com'
EMAIL_HOST_PASSWORD = 'WeShareHere001'
# EMAIL_USE_TLS = True
EMAIL_SSL_PORT = 465



DEFAULT_ICON = "/files/icons/c0f8af6b6e5670f4f229abc2c964899e.jpeg"


SALT = 'hetongshinanshen'
TENCENT_APPID = 101340075
TENCENT_APPKEY = '8a66f6a4a93ef09b970afd245ed8b8fc'
