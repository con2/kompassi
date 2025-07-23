import logging

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError
from oauth2_provider.models import Application

from kompassi.core.models import Person

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    def handle(*args, **options):
        if settings.DEBUG:
            person, unused = Person.get_or_create_dummy()

            try:
                Application.objects.get_or_create(
                    client_id="kompassi_insecure_test_client_id",
                    defaults=dict(
                        user=person.user,
                        redirect_uris="\n".join(
                            [
                                # kompassi2, edegal etc.
                                "http://localhost:3000/api/auth/callback/kompassi",
                            ]
                        ),
                        client_type="confidential",  # hah
                        authorization_grant_type="authorization-code",
                        client_secret="kompassi_insecure_test_client_secret",
                        name="Insecure test application",
                        algorithm="RS256",
                        skip_authorization=True,
                    ),
                )
            except IntegrityError:
                # get_or_create fails to recognize collision on hash_client_secret
                logger.exception("Failed to create insecure test application")
                pass
