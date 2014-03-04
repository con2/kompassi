# encoding: utf-8

import os
from datetime import datetime, timedelta

import django.conf.global_settings as defaults

from dateutil.tz import tzlocal


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
#     'default' : dict(
#         BACKEND = 'johnny.backends.memcached.MemcachedCache',
#         LOCATION = ['127.0.0.1:11211'],
#         JOHNNY_CACHE = True,
#     )
# }

ALLOWED_HOSTS = []

TIME_ZONE = 'Europe/Helsinki'
DATETIME_FORMAT = 'd.m.y H:i'
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
    # Uncomment if you have memcached
    # 'johnny.middleware.LocalStoreClearMiddleware',
    # 'johnny.middleware.QueryCacheMiddleware',

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

    'tracon8',
    'tracon9',
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
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
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

LOGIN_URL = '/login'

tz = tzlocal()

# XXX this should go in the database
# Tracon 8 specific
TIMETABLE_TIME_BLOCKS = [
    (
        datetime(2013, 9, 14, 11, 0, 0, tzinfo=tz),
        datetime(2013, 9, 15, 1 , 0, 0, tzinfo=tz)
    ),
    (
        datetime(2013, 9, 15, 9 , 0, 0, tzinfo=tz),
        datetime(2013, 9, 15, 17, 0, 0, tzinfo=tz)
    )
]
TIMETABLE_SPECIAL_TIMES = [
    datetime(2013, 9, 14, 10, 30, 0, tzinfo=tz)
]

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

TURSKA_INSTALLATION_NAME = u'Turska (DEV)'
TURSKA_INSTALLATION_NAME_ILLATIVE = u'Turskan kehitysinstanssiin'
TURSKA_INSTALLATION_SLUG = 'turskadev'
TURSKA_ACCOUNT_BRANDING = u'Tracon-tunnus'
TURSKA_ACCOUNT_BRANDING_PARTITIVE = u'Tracon-tunnusta'
TURSKA_ACCOUNT_BRANDING_2ND_PERSON_ADESSIVE = u'Tracon-tunnuksellasi'
TURSKA_ACCOUNT_INFO = u'Tracon-tunnus on uusi, keväällä 2014 käynnistetty projekti, joka yhdistää kaikki Traconin sähköiset palvelut yhden käyttäjätunnuksen ja salasanan taakse. Valitettavasti vanhat Jyrä-, Pora- ja Aniki-tunnukset eivät käy Tracon-tunnuksesta.'
TURSKA_PRIVACY_POLICY_URL = 'http://media.tracon.fi/2014/tracon9_turska_rekisteriseloste.pdf'

JOHNNY_MIDDLEWARE_KEY_PREFIX = TURSKA_INSTALLATION_SLUG

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)


# These MUST match those in IPA
TURSKA_PASSWORD_MIN_LENGTH = 8
TURSKA_PASSWORD_MIN_CLASSES = 2

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

    TURSKA_LDAP_DOMAIN = 'dc=tracon,dc=fi'
    TURSKA_LDAP_USERS = 'cn=users,cn=accounts,{TURSKA_LDAP_DOMAIN}'.format(**locals())
    TURSKA_LDAP_GROUPS = 'cn=groups,cn=accounts,{TURSKA_LDAP_DOMAIN}'.format(**locals())

    TURSKA_IPA_JSONRPC = 'https://moukari.tracon.fi/ipa/json'
    TURSKA_IPA_CACERT_PATH = '/etc/ipa/ca.crt'

    import ldap
    from django_auth_ldap.config import LDAPSearch, PosixGroupType, NestedGroupOfNamesType

    #AUTH_LDAP_SERVER_URI = "ldaps://moukari.tracon.fi"
    AUTH_LDAP_SERVER_URI = "ldaps://localhost:64636"

    # AUTH_LDAP_BIND_DN = ""
    # AUTH_LDAP_BIND_PASSWORD = ""
    # AUTH_LDAP_USER_DN_TEMPLATE = "uid=%(user)s,{TURSKA_LDAP_USERS}".format(**locals())
    AUTH_LDAP_USER_SEARCH = LDAPSearch(
        TURSKA_LDAP_USERS,
        ldap.SCOPE_SUBTREE,
        "(uid=%(user)s)"
    )
    AUTH_LDAP_ALWAYS_UPDATE_USER = True

    AUTH_LDAP_GROUP_SEARCH = LDAPSearch(
        TURSKA_LDAP_GROUPS,
        ldap.SCOPE_SUBTREE,
        "(objectClass=groupOfNames)"
    )
    AUTH_LDAP_GROUP_TYPE = NestedGroupOfNamesType()
    AUTH_LDAP_MIRROR_GROUPS = True

    AUTH_LDAP_REQUIRE_GROUP = "cn={TURSKA_INSTALLATION_SLUG}-users,{TURSKA_LDAP_GROUPS}".format(**locals())
    # AUTH_LDAP_DENY_GROUP = "cn={TURSKA_INSTALLATION_SLUG}-banned,{TURSKA_LDAP_GROUPS}".format(**locals())

    AUTH_LDAP_USER_FLAGS_BY_GROUP = {
        "is_active": "cn={TURSKA_INSTALLATION_SLUG}-users,{TURSKA_LDAP_GROUPS}".format(**locals()),
        "is_staff": "cn={TURSKA_INSTALLATION_SLUG}-staff,{TURSKA_LDAP_GROUPS}".format(**locals()),
        "is_superuser": "cn={TURSKA_INSTALLATION_SLUG}-admins,{TURSKA_LDAP_GROUPS}".format(**locals()),
    }

    AUTH_LDAP_USER_ATTR_MAP = {"first_name": "givenName", "last_name": "sn"}
    AUTH_LDAP_GLOBAL_OPTIONS = {
        ldap.OPT_X_TLS_REQUIRE_CERT: ldap.OPT_X_TLS_ALLOW,
        ldap.OPT_X_TLS_CACERTFILE: TURSKA_IPA_CACERT_PATH,
	    ldap.OPT_REFERRALS: 0,
    }

    from sets import Set
    TURSKA_NEW_USER_INITIAL_GROUPS = Set([
        "{TURSKA_INSTALLATION_SLUG}-users".format(**locals()),

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
