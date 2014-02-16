# Django settings for condb project.

import os
from datetime import datetime, timedelta

import django.conf.global_settings as defaults

from dateutil.tz import tzlocal


def mkpath(*parts):
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '..', *parts))


DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'condb.sqlite3',                      # Or path to database file if using sqlite3.
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

JOHNNY_MIDDLEWARE_KEY_PREFIX='condb_johnny_dev'

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = []

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Europe/Helsinki'
DATETIME_FORMAT = 'd.m.y H:i'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'fi-FI'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = mkpath('media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = mkpath('static')

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'jhdjl*kxcet2aaz)%ixmois*j_p+d*q79%legoz+9el(c%zc$%'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    ('pyjade.ext.django.Loader',(
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    )),
)

# add johnny's middleware
MIDDLEWARE_CLASSES = (
    # Uncomment if you have memcached
    # 'johnny.middleware.LocalStoreClearMiddleware',
    # 'johnny.middleware.QueryCacheMiddleware',

    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'condb.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'condb.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    mkpath('condb','templates'),
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
    'external_auth',

    'tracon8',
    'tracon9',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
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

CONDB_INSTALLATION_NAME = 'turskadev'

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)

CONDB_PASSWORD_MIN_LENGTH = 8
CONDB_PASSWORD_MIN_CLASSES = 2

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

    CONDB_LDAP_DOMAIN = 'dc=tracon,dc=fi'
    CONDB_LDAP_USERS = 'cn=users,cn=accounts,{CONDB_LDAP_DOMAIN}'.format(**locals())
    CONDB_LDAP_GROUPS = 'cn=groups,cn=accounts,{CONDB_LDAP_DOMAIN}'.format(**locals())

    CONDB_IPA_JSONRPC = 'https://moukari.tracon.fi/ipa/json'
    CONDB_IPA_CACERT_PATH = '/etc/ipa/ca.crt'

    import ldap
    from django_auth_ldap.config import LDAPSearch, PosixGroupType, GroupOfNamesType

    #AUTH_LDAP_SERVER_URI = "ldaps://moukari.tracon.fi"
    AUTH_LDAP_SERVER_URI = "ldaps://localhost:64636"
    
    # AUTH_LDAP_BIND_DN = ""
    # AUTH_LDAP_BIND_PASSWORD = ""
    # AUTH_LDAP_USER_DN_TEMPLATE = "uid=%(user)s,{CONDB_LDAP_USERS}".format(**locals())
    AUTH_LDAP_USER_SEARCH = LDAPSearch(
        CONDB_LDAP_USERS,
        ldap.SCOPE_SUBTREE,
        "(uid=%(user)s)"
    )
    AUTH_LDAP_ALWAYS_UPDATE_USER = True

    AUTH_LDAP_GROUP_SEARCH = LDAPSearch(
        CONDB_LDAP_GROUPS,
        ldap.SCOPE_SUBTREE,
        "(objectClass=groupOfNames)"
    )
    AUTH_LDAP_GROUP_TYPE = GroupOfNamesType()
    AUTH_LDAP_MIRROR_GROUPS = True

    AUTH_LDAP_REQUIRE_GROUP = "cn={CONDB_INSTALLATION_NAME}-users,{CONDB_LDAP_GROUPS}".format(**locals())
    # AUTH_LDAP_DENY_GROUP = "cn={CONDB_INSTALLATION_NAME}-banned,{CONDB_LDAP_GROUPS}".format(**locals())

    AUTH_LDAP_USER_FLAGS_BY_GROUP = {
        "is_active": "cn={CONDB_INSTALLATION_NAME}-users,{CONDB_LDAP_GROUPS}".format(**locals()),
        "is_staff": "cn={CONDB_INSTALLATION_NAME}-admins,{CONDB_LDAP_GROUPS}".format(**locals()),
        "is_superuser": "cn={CONDB_INSTALLATION_NAME}-admins,{CONDB_LDAP_GROUPS}".format(**locals()),
    }

    AUTH_LDAP_USER_ATTR_MAP = {"first_name": "givenName", "last_name": "sn"}
    AUTH_LDAP_GLOBAL_OPTIONS = {
        ldap.OPT_X_TLS_REQUIRE_CERT: ldap.OPT_X_TLS_ALLOW,
        ldap.OPT_X_TLS_CACERTFILE: CONDB_IPA_CACERT_PATH,
	    ldap.OPT_REFERRALS: 0,
    }

    from sets import Set
    CONDB_NEW_USER_INITIAL_GROUPS = Set([
        "{CONDB_INSTALLATION_NAME}-users".format(**locals()),
        
        # to make sure users created via condbdev.tracon.fi can also access the
        # actual installation
        'turska-users',
    ])
