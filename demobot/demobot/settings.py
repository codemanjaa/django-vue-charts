"""
Django settings for demobot project.

Generated by 'django-admin startproject' using Django 2.2.3.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
from django.conf.global_settings import FIXTURE_DIRS

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '4!enp!w!^^t4j_=-vpoppexj_^seotdypu1tr^h^z*0li!*%*5'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
  'django.contrib.admin',
  'django.contrib.auth',
  'django.contrib.contenttypes',
  'django.contrib.sessions',
  'django.contrib.messages',
  'django.contrib.staticfiles',
  'app',
  'rest_framework',
  'webpack_loader',
  'corsheaders',

]

MIDDLEWARE = [
  'django.middleware.security.SecurityMiddleware',
  'django.contrib.sessions.middleware.SessionMiddleware',
  'django.middleware.common.CommonMiddleware',
  'django.middleware.csrf.CsrfViewMiddleware',
  'django.contrib.auth.middleware.AuthenticationMiddleware',
  'django.contrib.messages.middleware.MessageMiddleware',
  'django.middleware.clickjacking.XFrameOptionsMiddleware',
  'corsheaders.middleware.CorsMiddleware',
]

CORS_ORIGIN_WHITELIST = [
  "http://localhost:8080",
  "http://localhost:8000"
]

ROOT_URLCONF = 'demobot.urls'

TEMPLATES = [
  {
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [BASE_DIR],
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

WSGI_APPLICATION = 'demobot.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
  'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'auth.db')
        #'NAME': os.path.join(BASE_DIR, '../jdfbot-master/jdf.db'),
    },
  'jdf_db' :{
    'ENGINE': 'django.db.backends.sqlite3',
    #'NAME': os.path.join(BASE_DIR, 'jdfh.db'),
    'NAME': os.path.join(BASE_DIR, '../jdfbot-master/jdf.db'),
  }
}

#   'default': {
#     'ENGINE': 'django.db.backends.sqlite3',
#     'NAME': os.path.join(BASE_DIR, 'jdfh.db'),
#     #'NAME': os.path.join(BASE_DIR, '../jdfbot-master/jdf.db'),
#
#    },
#   'auth_db': {
#     'ENGINE': 'django.db.backends.sqlite3',
#     'NAME': os.path.join(BASE_DIR, 'jdfh.db'),
#     # 'NAME': os.path.join(BASE_DIR, '../jdfbot-master/jdf.db'),
#   },
#   'jdf_db': {
#     'ENGINE': 'django.db.backends.sqlite3',
#     #      # 'NAME': os.path.join(BASE_DIR, 'jdf.db'),
#     'NAME': os.path.join(BASE_DIR, '../jdfbot-master/jdf.db'),
#     #
#   },
# }

DATABASE_ROUTERS = ['app.models.AuthRouter','app.models.PrimaryRouter']
DATABASE_APPS_MAPPING = {'default':'auth','primary': 'jdf_db'}

FIXTURE_DIRS = ['fixtures']

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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

# Fixture setting


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

# STATIC_URL = '/static/'
STATIC_URL = '/public/'
STATIC_ROOT = os.path.join(BASE_DIR, 'vuesimple')
STATICFILES_DIRS = (
  os.path.join(BASE_DIR, '/dist'),
)
WEBPACK_LOADER = {
  'DEFAULT': {
    'CACHE': not DEBUG,
    'BUNDLE_DIR_NAME': '/',
    'STATS_FILE': os.path.join(BASE_DIR, 'vuesimple/webpack-stats.json'),
    'POLL_INTERVAL': 0.1,
    'TIMEOUT': None,
    'IGNORE': ['.+\.hot-update.js', '.+\.map']
  }
}
