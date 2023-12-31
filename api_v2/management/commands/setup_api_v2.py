from django.conf import settings
from django.core.management.base import BaseCommand

from oauth2_provider.models import Application

from core.models import Person


class Command(BaseCommand):
    def handle(*args, **options):
        if settings.DEBUG:
            person, unused = Person.get_or_create_dummy()

            algorithm = "RS256" if settings.OAUTH2_PROVIDER["OIDC_RSA_PRIVATE_KEY"] else None

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
                    algorithm=algorithm,
                    skip_authorization=True,
                ),
            )
