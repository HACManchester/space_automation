"""
Django settings for mcp project.

Generated by 'django-admin startproject' using Django 1.11.3.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

import ldap
from django_auth_ldap.config import LDAPSearch, GroupOfNamesType

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'x_hto3dh*&lt4vy5pp5n0_z$lzo!5_x@4az(@l_10@w_+i=s71'

ALLOWED_HOSTS = ['*']

DEBUG = os.environ.get('DEBUG') is not False

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'debug_toolbar',
    'localflavor',
    'user_auth',
    'access_control'
]

MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'mcp.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'mcp.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres',
        'HOST': 'db',
        'PORT': 5432,
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    ]

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

AUTH_LDAP_SERVER_URI = "ldaps://ldap.hacman.org.uk"

# AUTH_LDAP_BIND_AS_AUTHENTICATING_USER = True

AUTH_LDAP_BIND_DN = os.environ.get('AUTH_LDAP_BIND_DN')
AUTH_LDAP_BIND_PASSWORD = os.environ.get('AUTH_LDAP_BIND_PASSWORD')
AUTH_LDAP_USER_SEARCH = LDAPSearch("cn=accounts,dc=hacman,dc=org,dc=uk",
                                   ldap.SCOPE_SUBTREE, "(|(uid=%(user)s)(mail=%(user)s))")

# Set up the basic group parameters.
AUTH_LDAP_GROUP_SEARCH = LDAPSearch("cn=groups,cn=accounts,dc=hacman,dc=org,dc=uk",
                                    ldap.SCOPE_SUBTREE,
                                    "(&(objectClass=groupOfNames)(memberOf=cn=mcp,"
                                    "cn=groups,cn=accounts,dc=hacman,dc=org,dc=uk))")

AUTH_LDAP_GROUP_TYPE = GroupOfNamesType()

AUTH_LDAP_REQUIRE_GROUP = "cn=allusers,cn=groups,cn=accounts,dc=hacman,dc=org,dc=uk"

# Populate the Django user from the LDAP directory.
AUTH_LDAP_USER_ATTR_MAP = {
    "first_name": "givenName",
    "last_name": "sn",
    "email": "mail",
    "username": "uid"
}

AUTH_LDAP_USER_FLAGS_BY_GROUP = {
    "is_member": "cn=members,cn=groups,cn=accounts,dc=hacman,dc=org,dc=uk",
    "is_staff": "cn=mcp_useradmins,cn=groups,cn=accounts,dc=hacman,dc=org,dc=uk",
    "is_superuser": "cn=mcp_useradmins,cn=groups,cn=accounts,dc=hacman,dc=org,dc=uk"
}

AUTH_LDAP_FIND_GROUP_PERMS = True

AUTH_LDAP_CACHE_GROUPS = True
AUTH_LDAP_GROUP_CACHE_TIMEOUT = 60

AUTH_LDAP_MIRROR_GROUPS = True

# Keep ModelBackend around for local superuser
AUTHENTICATION_BACKENDS = (
    'mcp.ldap.LDAPMergeBackend',
    'django.contrib.auth.backends.ModelBackend',
)

# GoCardless
GC_ACCESS_TOKEN = os.environ.get('GC_ACCESS_TOKEN')

# Where can a user log in?
LOGIN_URL = '/'
LOGIN_REDIRECT_URL = '/test'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'stream_to_console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler'
        },
    },
    'loggers': {
        'django_auth_ldap': {
            'handlers': ['stream_to_console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    }
}

INTERNAL_IPS = ['172.18.0.1']
