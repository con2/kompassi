import logging
from contextlib import contextmanager
from uuid import uuid4

from django.conf import settings
from django.core.cache import cache
from django.core.management import call_command, get_commands
from django.core.management.base import BaseCommand
from django.db.transaction import atomic

logger = logging.getLogger("kompassi")


@contextmanager
def noop_context():
    yield


def setup_should_run(run_id=settings.KOMPASSI_SETUP_RUN_ID, expire_seconds=settings.KOMPASSI_SETUP_EXPIRE_SECONDS):
    """
    When deployed under Kubernetes and using multiple replicas, we want only the first replica
    to perform the setup. This is achieved using an environment variable KOMPASSI_SETUP_RUN_ID
    that is filled in in the Deployment to contain the pod template hash.
    """
    if not run_id:
        logger.info("manage.py setup: KOMPASSI_SETUP_RUN_ID not supplied, running unconditionally.")
        return True

    cache_key = f"kompassi:setup_should_run:{run_id}"
    nonce = str(uuid4())

    try:
        # Redis SETNX: True iff the key wasn't already set and we were able to set it
        return cache.set(cache_key, nonce, expire_seconds, nx=True)  # type: ignore
    except Exception:
        logger.exception("manage.py setup: setup_should_run failed to determine, running anyway")
        # Something went wrong. Perhaps the cache is not Redis or the cache is unable to perform.
        # It's safer to run the setup than not run it.
        return True


class Command(BaseCommand):
    args = ""
    help = "Setup all the things"

    def handle(self, *args, **options):
        if not setup_should_run():
            logger.info(f"manage.py setup: has already run for {settings.KOMPASSI_SETUP_RUN_ID}, doing nothing")
            return

        commands = get_commands()

        organizations = [
            app_name.split(".")[-1] for app_name in settings.INSTALLED_APPS if app_name.startswith("organizations.")
        ]
        organization_commands = [
            command for command in (f"setup_{organization}" for organization in organizations) if command in commands
        ]

        events = [app_name.split(".")[-1] for app_name in settings.INSTALLED_APPS if app_name.startswith("events.")]
        event_commands = [command for command in (f"setup_{event}" for event in events) if command in commands]

        management_commands = [
            # (('kompassi_i18n', '-acv2'), dict()),
            # (('collectstatic',), dict(interactive=False)),
            (("migrate",), dict(interactive=False)),
            # must come before other setup_* commands because they may emit event log entries
            (("setup_event_log_v2",), dict()),
            (("setup_core",), dict()),
            (("setup_labour_common_qualifications",), dict()),
            (("setup_api_v2",), dict()),
            (("setup_access",), dict()),
            (("setup_emprinten",), dict()),
        ]

        management_commands.extend(((command,), dict()) for command in organization_commands)
        management_commands.extend(((command,), dict()) for command in event_commands)

        management_commands.extend(
            (
                (("setup_listings",), dict()),
                (("access_create_internal_aliases",), dict()),
                (("access_create_missing_cbac_entries",), dict()),
                (("access_prune_expired_cbac_entries",), dict()),
                (("forms_refresh_enriched_fields",), dict()),
                (("clearsessions",), dict()),
            )
        )

        for pargs, opts in management_commands:
            print("** Running:", pargs[0])
            with atomic() if pargs[0].startswith("setup") else noop_context():
                call_command(*pargs, **opts)
