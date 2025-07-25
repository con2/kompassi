import warnings
from email.utils import parseaddr
from pathlib import Path

import environ
from csp.constants import NONE, SELF, UNSAFE_EVAL, UNSAFE_INLINE
from django.contrib.messages import constants as messages
from django.utils.translation import gettext_lazy as _

from kompassi.tickets_v2 import lippukala_integration

env = environ.Env(
    DEBUG=(bool, False),
)  # set default values and casting

# silence warning from .env not existing
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    environ.Env.read_env()  # reading .env file


DEBUG = env.bool("DEBUG", default=False)

CORS_ORIGIN_ALLOW_ALL = DEBUG
CORS_URLS_REGEX = r"^/(api|oauth2|oidc)/.*$"
CORS_ORIGIN_WHITELIST = env("CORS_ORIGIN_WHITELIST", default="").split()

# /login?next= and /register?next= as protected by CSP
KOMPASSI_CSP_ALLOWED_LOGIN_REDIRECTS = env("KOMPASSI_CSP_ALLOWED_LOGIN_REDIRECTS", default="").split()

ADMINS = [parseaddr(addr) for addr in env("ADMINS", default="").split(",") if addr]

MANAGERS = ADMINS

DATABASES = {
    "default": {
        "HOST": env("POSTGRES_HOSTNAME", default="postgres"),
        "NAME": env("POSTGRES_DATABASE", default="kompassi"),
        "USER": env("POSTGRES_USERNAME", default="kompassi"),
        "PORT": env("POSTGRES_PORT", default="5432"),
        "PASSWORD": env("POSTGRES_PASSWORD", default="secret"),
        "OPTIONS": {
            "sslmode": env("POSTGRES_SSLMODE", default="allow"),
        },
        "ENGINE": "django.db.backends.postgresql",
    },
}

SESSION_ENGINE = "django.contrib.sessions.backends.cache"

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

CACHES = {
    "default": env.cache(default="locmemcache://"),
}

ALLOWED_HOSTS = env("ALLOWED_HOSTS", default="localhost").split()

TIME_ZONE = "Europe/Helsinki"

DATE_FORMAT = "j.n.Y"
SHORT_DATE_FORMAT = DATE_FORMAT
DATE_FORMAT_STRFTIME = "%d.%m.%Y"

DATETIME_FORMAT = "j.n.Y G:i:s"
SHORT_DATETIME_FORMAT = DATETIME_FORMAT
DATETIME_FORMAT_STRFTIME = "%d.%m.%Y %H:%M:%S"

LANGUAGE_CODE = "en"
LANGUAGES = (
    ("fi", _("Finnish")),
    ("en", _("English")),
)
SITE_ID = 1
USE_I18N = True
USE_TZ = True

MEDIA_ROOT = Path(__file__).with_name("media")
MEDIA_URL = "/media/"
STATIC_ROOT = Path(__file__).with_name("static")
STATIC_URL = "/static/"

STATICFILES_DIRS = ()
STORAGES = {
    "default": {
        "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}
STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    # 'django.contrib.staticfiles.finders.DefaultStorageFinder',
)


SECRET_KEY = env.str("SECRET_KEY", default=("" if not DEBUG else "xxx"))

MIDDLEWARE = (
    "corsheaders.middleware.CorsMiddleware",
    "csp.middleware.CSPMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "kompassi.listings.middleware.ListingsMiddleware",
    "kompassi.core.middleware.request_cache_middleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "oauth2_provider.middleware.OAuth2TokenMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.locale.LocaleMiddleware",
)

ROOT_URLCONF = "kompassi.urls"
WSGI_APPLICATION = "kompassi.wsgi.application"
APPEND_SLASH = False
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")


TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "OPTIONS": {
            "context_processors": [
                "kompassi.core.context_processors.core_context",
                "kompassi.feedback.context_processors.feedback_context",
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
            "loaders": [
                (
                    "pypugjs.ext.django.Loader",
                    (
                        "django.template.loaders.filesystem.Loader",
                        "django.template.loaders.app_directories.Loader",
                    ),
                )
            ],
            "builtins": [
                "pypugjs.ext.django.templatetags",
            ],
        },
    },
]

TEST_RUNNER = "django.test.runner.DiscoverRunner"

INSTALLED_APPS = (
    # django core apps
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.admin",
    "django.contrib.postgres",
    "django.contrib.humanize",
    # 3rd party apps
    "pypugjs.ext.django",
    "crispy_forms",
    "crispy_bootstrap3",
    "oauth2_provider",
    "bootstrap3",
    "graphene_django",
    # 1st party embedded apps
    "lippukala",
    "paikkala",
    # kompassi core apps
    "kompassi.core",
    "kompassi.dimensions",
    "kompassi.involvement",
    "kompassi.program_v2",
    "kompassi.labour",
    "kompassi.labour_common_qualifications",
    "kompassi.tickets_v2",
    "kompassi.payments",
    "kompassi.mailings",
    "kompassi.api",
    "kompassi.api_v2",
    "kompassi.graphql_api",
    "kompassi.badges",
    "kompassi.access",
    "kompassi.membership",
    "kompassi.intra",
    "kompassi.desuprofile_integration",
    "kompassi.feedback",
    "kompassi.event_log_v2",
    "kompassi.directory",
    "kompassi.listings",
    "kompassi.forms",
    "kompassi.metrics",
    "kompassi.emprinten",
    # organizations
    "kompassi.organizations.tracon_ry",
    "kompassi.organizations.kotae_ry",
    "kompassi.organizations.ropecon_ry",
    "kompassi.organizations.cosmocon_ry",
    # events
    "kompassi.events.kuplii2018",
    "kompassi.events.tracon2018",
    "kompassi.events.popcultday2018",
    "kompassi.events.matsucon2018",
    "kompassi.events.ropecon2018",
    "kompassi.events.finncon2018",
    "kompassi.events.frostbite2019",
    "kompassi.events.desucon2019",
    "kompassi.events.tracon2019",
    "kompassi.events.finncon2020",
    "kompassi.events.kuplii2019",
    "kompassi.events.nekocon2019",
    "kompassi.events.popcult2019",
    "kompassi.events.hitpoint2019",
    "kompassi.events.hypecon2019",
    "kompassi.events.ropecon2019",
    "kompassi.events.matsucon2019",
    "kompassi.events.finncon2019",
    "kompassi.events.popcultnights2019",
    "kompassi.events.frostbite2020",
    "kompassi.events.desucon2020",
    "kompassi.events.kuplii2020",
    "kompassi.events.tracon2020",
    "kompassi.events.nekocon2020",
    "kompassi.events.ropecon2020",
    "kompassi.events.tracrossf2019",
    "kompassi.events.hypecon2020",
    "kompassi.events.popcult2020",
    "kompassi.events.matsucon2020",
    "kompassi.events.hitpoint2020",
    "kompassi.events.ropecon2020vd",
    "kompassi.events.ropecon2021",
    "kompassi.events.tracon2021",
    "kompassi.events.kuplii2021",
    "kompassi.events.ropeconjvp2021",
    "kompassi.events.desucon2022",
    "kompassi.events.ropecon2022",
    "kompassi.events.tracon2022",
    "kompassi.events.kuplii2022",
    "kompassi.events.finncon2022",
    "kompassi.events.nekocon2022",
    "kompassi.events.traconjvp2022",
    "kompassi.events.traconjvk2022",
    "kompassi.events.frostbite2023",
    "kompassi.events.desucon2023",
    "kompassi.events.matsucon2022",
    "kompassi.events.tracon2023",
    "kompassi.events.ropecon2023",
    "kompassi.events.kuplii2023",
    "kompassi.events.hitpoint2023",
    "kompassi.events.nekocon2023",
    "kompassi.events.finncon2023",
    "kompassi.events.cosvision2023",
    "kompassi.events.shumicon2023",
    "kompassi.events.shumicon2025",
    "kompassi.events.matsucon2023",
    "kompassi.events.popcultnights2023",
    "kompassi.events.kotaeexpo2024",
    "kompassi.events.frostbite2024",
    "kompassi.events.desucon2024",
    "kompassi.events.tracon2024",
    "kompassi.events.kuplii2024",
    "kompassi.events.solmukohta2024",
    "kompassi.events.hitpoint2024",
    "kompassi.events.ropecon2024",
    "kompassi.events.popcultday2024",
    "kompassi.events.matsucon2024",
    "kompassi.events.ropecon2025",
    "kompassi.events.frostbite2025",
    "kompassi.events.desucon2025",
    "kompassi.events.kotaeexpo2025",
    "kompassi.events.popcultnights2024",
    "kompassi.events.tracon2025",
    "kompassi.events.cosmocon2025",
    "kompassi.events.kuplii2025",
    "kompassi.events.matsucon2025",
    "kompassi.events.archipelacon2025",
    "kompassi.events.popcultnights2025",
    # zombies are obsolete apps that can't be removed due to cross-app references in models
    "kompassi.zombies.enrollment",
    "kompassi.zombies.event_log",
    "kompassi.zombies.programme",
    "kompassi.zombies.surveys",
    "kompassi.zombies.tickets",
    "kompassi.zombies.hitpoint2017",
)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {"format": "%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s"},
        "simple": {"format": "%(levelname)s %(message)s"},
    },
    "filters": {"require_debug_false": {"()": "django.utils.log.RequireDebugFalse"}},
    "handlers": {
        "mail_admins": {
            "level": "ERROR",
            "filters": ["require_debug_false"],
            "class": "django.utils.log.AdminEmailHandler",
        },
        "console": {
            "level": "DEBUG" if DEBUG else "INFO",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "loggers": {
        "django.request": {
            "handlers": ["console", "mail_admins"],
            "level": "ERROR",
            "propagate": True,
        },
        "celery": {
            "handlers": ["console"],
            "level": "DEBUG" if DEBUG else "WARNING",
            "propagate": True,
        },
        "kompassi": {
            "handlers": ["console"],
            "level": "DEBUG" if DEBUG else "INFO",
            "propagate": True,
        },
        "requests": {
            "handlers": ["console"],
            "level": "DEBUG" if DEBUG else "WARNING",
            "propagate": True,
        },
    },
}

GRAPHENE = {
    "SCHEMA": "graphql_api.schema.schema",
    "MIDDLEWARE": [
        "kompassi.graphql_api.graphene_middleware.LoggingErrorsMiddleware",
    ],
}

LOGIN_URL = "/login"

CRISPY_TEMPLATE_PACK = "bootstrap3"

AWS_STORAGE_BUCKET_NAME = env("MINIO_BUCKET_NAME", default="kompassi")
AWS_ACCESS_KEY_ID = env("MINIO_ACCESS_KEY_ID", default="kompassi")
AWS_SECRET_ACCESS_KEY = env("MINIO_SECRET_ACCESS_KEY", default="kompassi")
AWS_S3_ENDPOINT_URL = env("MINIO_ENDPOINT_URL", default="http://localhost:9000")

KOMPASSI_BASE_URL = env("KOMPASSI_BASE_URL", default="http://localhost:8000")
KOMPASSI_V2_BASE_URL = env("KOMPASSI_V2_BASE_URL", default="http://localhost:3000")

# TODO script-src unsafe-inline needed at least by feedback.js. unsafe-eval needed by Knockout (roster.js).
CONTENT_SECURITY_POLICY = {
    "DIRECTIVES": {
        "default-src": [NONE],
        "script-src": [SELF, UNSAFE_INLINE, UNSAFE_EVAL],  # XXX unsafe-inline should be eradicated.
        "connect-src": [SELF],
        "img-src": [SELF, AWS_S3_ENDPOINT_URL],
        "style-src": [SELF, UNSAFE_INLINE],  # XXX unsafe-inline should be eradicated.
        "font-src": [SELF],
        "form-action": [SELF, KOMPASSI_V2_BASE_URL],
        "frame-ancestors": [NONE],
    }
}
X_FRAME_OPTIONS = "DENY"


MESSAGE_TAGS = {
    messages.ERROR: "danger",
}


KOMPASSI_APPLICATION_NAME = "Kompassi"
KOMPASSI_INSTALLATION_NAME = env("KOMPASSI_INSTALLATION_NAME", default="Kompassi (DEV)")
KOMPASSI_INSTALLATION_NAME_ILLATIVE = "Kompassin kehitys\u00adinstanssiin" if DEBUG else "Kompassiin"
KOMPASSI_INSTALLATION_NAME_GENITIVE = "Kompassin kehitys\u00adinstanssin" if DEBUG else "Kompassin"
KOMPASSI_INSTALLATION_NAME_PARTITIVE = "Kompassin kehitys\u00adinstanssia" if DEBUG else "Kompassia"
KOMPASSI_INSTALLATION_SLUG = env("KOMPASSI_INSTALLATION_SLUG", default="turskadev")
KOMPASSI_PRIVACY_POLICY_URL = "https://tracon.fi/tietosuoja"
FEEDBACK_PRIVACY_POLICY_URL = "https://tracon.fi/tietosuoja"

# Confluence & co. require a group of users
KOMPASSI_NEW_USER_GROUPS = ["users"]
KOMPASSI_MAY_SEND_INFO_GROUP_NAME = "kompassi-maysendinfo"

AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "oauth2_provider.backends.OAuth2Backend",
)


# Default region for parsing phone numbers
# Passed as the second argument to python-phonenumbers' .parse
KOMPASSI_PHONENUMBERS_DEFAULT_REGION = "FI"

# Default format for normalizing phone numbers
# getattr'd from phonenumbers.PhoneNumberFormat with itself as default
KOMPASSI_PHONENUMBERS_DEFAULT_FORMAT = "INTERNATIONAL"


# Sending email
if env("EMAIL_HOST", default=""):
    EMAIL_HOST = env("EMAIL_HOST")
else:
    EMAIL_BACKEND = "django.core.mail.backends.dummy.EmailBackend"

DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL", default="spam@example.com")
SERVER_EMAIL = DEFAULT_FROM_EMAIL


LIPPUKALA_PREFIXES = lippukala_integration.PREFIXES
LIPPUKALA_LITERATE_KEYSPACES = lippukala_integration.KEYSPACES

LIPPUKALA_CODE_MIN_N_DIGITS = 7
LIPPUKALA_CODE_MAX_N_DIGITS = 7

# NOTE these will be overridden by the respective fields in TicketsEventMeta
# however, they need to be defined in settings or lippukala will barf.
LIPPUKALA_PRINT_LOGO_PATH = Path(__file__).parent / "core" / "static" / "jean_victor_balin_icon_star_24px.png"
LIPPUKALA_PRINT_LOGO_SIZE_CM = (3.0, 3.0)


if env("BROKER_URL", default=""):
    CELERY_BROKER_URL = env("BROKER_URL")
    CELERY_RESULT_BACKEND = CELERY_BROKER_URL
else:
    CELERY_BROKER_URL = "memory://"
    CELERY_RESULT_BACKEND = "cache+memory://"
    CELERY_TASK_ALWAYS_EAGER = True

CELERY_ACCEPT_CONTENT = ["json"]

CELERY_SEND_TASK_ERROR_EMAILS = not DEBUG
CELERY_SERVER_EMAIL = DEFAULT_FROM_EMAIL

CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"

CELERY_REDIS_SOCKET_KEEPALIVE = True

# kompassi.api
KOMPASSI_APPLICATION_USER_GROUP = f"{KOMPASSI_INSTALLATION_SLUG}-apps"


OAUTH2_PROVIDER = dict(
    OIDC_ENABLED=True,
    OIDC_RP_INITIATED_LOGOUT_ENABLED=True,
    OIDC_RP_INITIATED_LOGOUT_ALWAYS_PROMPT=False,
    OAUTH2_VALIDATOR_CLASS="kompassi.api_v2.custom_oauth2_validator.CustomOAuth2Validator",
    SCOPES=dict(
        # oidc scope (this is really the only one needed)
        openid="Kirjautua sisään muihin sovelluksiin",
        # some oidc apps assume email and profile scopes
        email="Tietää sähköpostiosoitteesi",
        profile="Tietää nimesi, sähköpostiosoitteesi, puhelinnumerosi ja syntymäaikasi",
        # legacy oauth2 scopes
        read="Tietää nimesi, sähköpostiosoitteesi, puhelinnumerosi ja syntymäaikasi",
        write="Muokata käyttäjä- ja henkilötietojasi",
    ),
    PKCE_REQUIRED=False,
    OIDC_RSA_PRIVATE_KEY=env("OIDC_RSA_PRIVATE_KEY", default=""),
)

# if True, users must verify their email address before they can log in to other services via Kompassi
KOMPASSI_OIDC_EMAIL_VERIFICATION_REQUIRED = False

# kompassi.desuprofile_integration
KOMPASSI_DESUPROFILE_HOST = env("KOMPASSI_DESUPROFILE_HOST", default="https://desucon.fi")
KOMPASSI_DESUPROFILE_OAUTH2_CLIENT_ID = env(
    "KOMPASSI_DESUPROFILE_OAUTH2_CLIENT_ID", default="kompassi_insecure_client_id"
)
KOMPASSI_DESUPROFILE_OAUTH2_CLIENT_SECRET = env(
    "KOMPASSI_DESUPROFILE_OAUTH2_CLIENT_SECRET",
    default="kompassi_insecure_client_secret",
)
KOMPASSI_DESUPROFILE_OAUTH2_SCOPE = ["read"]
KOMPASSI_DESUPROFILE_OAUTH2_AUTHORIZATION_URL = f"{KOMPASSI_DESUPROFILE_HOST}/oauth2/authorize/"
KOMPASSI_DESUPROFILE_OAUTH2_TOKEN_URL = f"{KOMPASSI_DESUPROFILE_HOST}/oauth2/token/"
KOMPASSI_DESUPROFILE_API_URL = f"{KOMPASSI_DESUPROFILE_HOST}/api/user/me/"


KOMPASSI_LISTING_URLCONFS = {
    "conit.fi": "kompassi.listings.site_urlconfs.conit_fi",
}


# Used by access.SMTPServer. Must be created with ssh-keygen -t rsa -m pem (will not work without -m pem).
KOMPASSI_SSH_PRIVATE_KEY_FILE = env("KOMPASSI_SSH_PRIVATE_KEY_FILE", default="/mnt/secrets/kompassi/sshPrivateKey")
KOMPASSI_SSH_KNOWN_HOSTS_FILE = env("KOMPASSI_SSH_KNOWN_HOSTS_FILE", default="/mnt/secrets/kompassi/sshKnownHosts")

# used by manage.py setup to noop if already run for this deploy
KOMPASSI_SETUP_RUN_ID = env("KOMPASSI_SETUP_RUN_ID", default="")
KOMPASSI_SETUP_EXPIRE_SECONDS = 300
