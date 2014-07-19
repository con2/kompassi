# encoding: utf-8
from __future__ import absolute_import

import os
from datetime import datetime, timedelta

import django.conf.global_settings as defaults


def mkpath(*parts):
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '..', *parts))


MKPATH = mkpath

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'turska.sqlite3',                      # Or path to database file if using sqlite3.
        'USER': '',
        'PASSWORD': '',
        'HOST': '',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '',                      # Set to empty string for default.
    }
}

# Uncomment if you have memcached
# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
#         'LOCATION': [
#             '127.0.0.1:11211'
#         ]
#     }
# }

ALLOWED_HOSTS = []

TIME_ZONE = 'Europe/Helsinki'
DATETIME_FORMAT = SHORT_DATETIME_FORMAT = 'd.m.Y H:i'
LANGUAGE_CODE = 'fi-FI'

SITE_ID = 1

USE_I18N = True
USE_L10N = True
USE_TZ = True

MEDIA_ROOT = mkpath('media')
MEDIA_URL = '/media/'
STATIC_ROOT = mkpath('static')
STATIC_URL = '/static/'

STATICFILES_DIRS = (
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

SECRET_KEY = 'jhdjl*kxcet2aaz)%ixmois*j_p+d*q79%legoz+9el(c%zc$%'

TEMPLATE_LOADERS = (
    ('pyjade.ext.django.Loader',(
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    )),
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',

    'core.middleware.PageWizardMiddleware',
)

ROOT_URLCONF = 'turska.urls'
WSGI_APPLICATION = 'turska.wsgi.application'

TEMPLATE_DIRS = (
    mkpath('turska','templates'),
)

TEMPLATE_CONTEXT_PROCESSORS = defaults.TEMPLATE_CONTEXT_PROCESSORS + (
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',
    'core.context_processors.core_context',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',

    'south',
    'pyjade',
    'crispy_forms',

    'core',
    'programme',
    'labour',
    'labour_common_qualifications',
    'tickets',
    'payments',
    'mailings',

    # Uncomment if you have IPA
    #'external_auth',

    # Uncomment if you do PDF tickets
    #'lippukala',

    # Uncomment if you have Celery
    # 'background_tasks',

    # Uncomment if you have Crowd and Confluence
    # 'atlassian_integration',

    'tracon_branding',
    'tracon8',
    'tracon9',
    'kawacon2014',
    'concon9',
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console':{
            'level': 'DEBUG' if DEBUG else 'WARNING',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'celery': {
            'handlers': ['console'],
            'level': 'DEBUG' if DEBUG else 'WARNING',
            'propagate': True
        },
        'atlassian_integration.utils': {
            'handlers': ['console'],
            'level': 'DEBUG' if DEBUG else 'WARNING',
            'propagate': True        
        }
    }
}

LOGIN_URL = '/login'

CRISPY_TEMPLATE_PACK = 'bootstrap3'

from django.contrib.messages import constants as messages
MESSAGE_TAGS = {
    messages.ERROR: 'danger',
}

DATE_FORMAT = 'j.n.Y'
DATE_FORMAT_STRFTIME = '%d.%m.%Y'

DATETIME_FORMAT = 'j.n.Y G:i:s'
DATETIME_FORMAT_STRFTIME = '%d.%m.%Y %H:%M:%S'

USE_L10N = True

KOMPASSI_APPLICATION_NAME = u'Kompassi'
KOMPASSI_INSTALLATION_NAME = u'Kompassi (DEV)'
KOMPASSI_INSTALLATION_NAME_ILLATIVE = u'Kompassin kehitysinstanssiin'
KOMPASSI_INSTALLATION_NAME_GENITIVE = u'Kompassin kehitysinstanssin'
KOMPASSI_INSTALLATION_SLUG = 'turskadev'
KOMPASSI_ACCOUNT_BRANDING = u'Tracon-tunnus'
KOMPASSI_ACCOUNT_BRANDING_PARTITIVE = u'Tracon-tunnusta'
KOMPASSI_ACCOUNT_BRANDING_ADESSIVE = u'Tracon-tunnuksella'
KOMPASSI_ACCOUNT_BRANDING_2ND_PERSON_ADESSIVE = u'Tracon-tunnuksellasi'
KOMPASSI_ACCOUNT_INFO = u'Tracon-tunnus on uusi, keväällä 2014 käynnistetty projekti, joka yhdistää kaikki Traconin sähköiset palvelut yhden käyttäjätunnuksen ja salasanan taakse. Valitettavasti vanhat Jyrä-, Pora- ja Aniki-tunnukset eivät käy Tracon-tunnuksesta.'
KOMPASSI_PRIVACY_POLICY_URL = 'http://media.tracon.fi/2014/tracon9_turska_rekisteriseloste.pdf'

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)


# These MUST match those in IPA
KOMPASSI_PASSWORD_MIN_LENGTH = 8
KOMPASSI_PASSWORD_MIN_CLASSES = 2

# Don't actually send email
EMAIL_BACKEND = 'django.core.mail.backends.dummy.EmailBackend'
DEFAULT_FROM_EMAIL = 'turska@tracon.fi'


if 'external_auth' in INSTALLED_APPS:
    # in case of emergency, break glass
    if DEBUG:
        import logging

        logger = logging.getLogger('django_auth_ldap')
        logger.addHandler(logging.StreamHandler())
        logger.setLevel(logging.DEBUG)

    AUTHENTICATION_BACKENDS = (
        'django_auth_ldap.backend.LDAPBackend',
    ) + AUTHENTICATION_BACKENDS

    KOMPASSI_LDAP_DOMAIN = 'dc=tracon,dc=fi'
    KOMPASSI_LDAP_USERS = 'cn=users,cn=accounts,{KOMPASSI_LDAP_DOMAIN}'.format(**locals())
    KOMPASSI_LDAP_GROUPS = 'cn=groups,cn=accounts,{KOMPASSI_LDAP_DOMAIN}'.format(**locals())

    KOMPASSI_IPA_JSONRPC = 'https://moukari.tracon.fi/ipa/json'
    KOMPASSI_IPA_CACERT_PATH = '/etc/ipa/ca.crt'

    import ldap
    from django_auth_ldap.config import LDAPSearch, PosixGroupType, NestedGroupOfNamesType

    #AUTH_LDAP_SERVER_URI = "ldaps://moukari.tracon.fi"
    AUTH_LDAP_SERVER_URI = "ldaps://localhost:64636"

    # AUTH_LDAP_BIND_DN = ""
    # AUTH_LDAP_BIND_PASSWORD = ""
    # AUTH_LDAP_USER_DN_TEMPLATE = "uid=%(user)s,{KOMPASSI_LDAP_USERS}".format(**locals())
    AUTH_LDAP_USER_SEARCH = LDAPSearch(
        KOMPASSI_LDAP_USERS,
        ldap.SCOPE_SUBTREE,
        "(uid=%(user)s)"
    )
    AUTH_LDAP_ALWAYS_UPDATE_USER = True

    AUTH_LDAP_GROUP_SEARCH = LDAPSearch(
        KOMPASSI_LDAP_GROUPS,
        ldap.SCOPE_SUBTREE,
        "(objectClass=groupOfNames)"
    )
    AUTH_LDAP_GROUP_TYPE = NestedGroupOfNamesType()
    AUTH_LDAP_MIRROR_GROUPS = True

    AUTH_LDAP_REQUIRE_GROUP = "cn={KOMPASSI_INSTALLATION_SLUG}-users,{KOMPASSI_LDAP_GROUPS}".format(**locals())
    # AUTH_LDAP_DENY_GROUP = "cn={KOMPASSI_INSTALLATION_SLUG}-banned,{KOMPASSI_LDAP_GROUPS}".format(**locals())

    AUTH_LDAP_USER_FLAGS_BY_GROUP = {
        "is_active": "cn={KOMPASSI_INSTALLATION_SLUG}-users,{KOMPASSI_LDAP_GROUPS}".format(**locals()),
        "is_staff": "cn={KOMPASSI_INSTALLATION_SLUG}-staff,{KOMPASSI_LDAP_GROUPS}".format(**locals()),
        "is_superuser": "cn={KOMPASSI_INSTALLATION_SLUG}-admins,{KOMPASSI_LDAP_GROUPS}".format(**locals()),
    }

    AUTH_LDAP_USER_ATTR_MAP = {"first_name": "givenName", "last_name": "sn"}
    AUTH_LDAP_GLOBAL_OPTIONS = {
        ldap.OPT_X_TLS_REQUIRE_CERT: ldap.OPT_X_TLS_ALLOW,
        ldap.OPT_X_TLS_CACERTFILE: KOMPASSI_IPA_CACERT_PATH,
	    ldap.OPT_REFERRALS: 0,
    }

    from sets import Set
    KOMPASSI_NEW_USER_INITIAL_GROUPS = Set([
        "{KOMPASSI_INSTALLATION_SLUG}-users".format(**locals()),

        # to make sure users created via turskadev.tracon.fi can also access the
        # actual installation
        'turska-users',
    ])


if 'payments' in INSTALLED_APPS:
    from payments.defaults import CHECKOUT_PARAMS
    CHECKOUT_PARAMS = dict(CHECKOUT_PARAMS,
        PASSWORD='SAIPPUAKAUPPIAS', # test account
        MERCHANT='375917', # test account
        DELIVERY_DATE='20130914' # Tracon 8 start
    )


if 'lippukala' in INSTALLED_APPS:
    # XXX event specific, move to the database
    import tracon9.lippukala_integration

    LIPPUKALA_PREFIXES = tracon9.lippukala_integration.PREFIXES
    LIPPUKALA_LITERATE_KEYSPACES = tracon9.lippukala_integration.KEYSPACES
    LIPPUTURSKA_QUEUE_SELECTOR = tracon9.lippukala_integration.select_queue

    LIPPUKALA_CODE_MIN_N_DIGITS = 7
    LIPPUKALA_CODE_MAX_N_DIGITS = 7

    LIPPUKALA_PRINT_LOGO_PATH = mkpath('static', 'images', 'tracon_logo_kuitille.jpg')
    LIPPUKALA_PRINT_LOGO_SIZE_CM = (5.84, 3.13)



if 'background_tasks' in INSTALLED_APPS:
    BROKER_URL = 'amqp://{KOMPASSI_INSTALLATION_SLUG}:{KOMPASSI_INSTALLATION_SLUG}@localhost/{KOMPASSI_INSTALLATION_SLUG}'.format(**locals())
    CELERY_ACCEPT_CONTENT = ['json']

    INSTALLED_APPS += (
        'djcelery',
        'djcelery_email',
    )

    #EMAIL_BACKEND = 'djcelery_email.backends.CeleryEmailBackend'

    CELERY_SEND_TASK_ERROR_EMAILS = not DEBUG
    SERVER_EMAIL = DEFAULT_FROM_EMAIL

    CELERY_TASK_SERIALIZER = 'json'
    CELERY_RESULT_SERIALIZER = 'json'


if 'atlassian_integration' in INSTALLED_APPS:
    KOMPASSI_CROWD_URL = 'https://crowd.tracon.fi/crowd'
    KOMPASSI_CROWD_APPLICATION_NAME = 'your application name here'
    KOMPASSI_CROWD_APPLICATION_PASSWORD = 'your application password here'
    KOMPASSI_CROWD_SESSION_URL = '{KOMPASSI_CROWD_URL}/rest/usermanagement/1/session'.format(**locals())
    KOMPASSI_CROWD_COOKIE_ATTRS = dict(
        key='crowd.token_key',
        httponly=True,
        secure=True,
        domain='.tracon.fi',
        path='/',
    )
    KOMPASSI_CONFLUENCE_URL = 'https://confluence.tracon.fi'
