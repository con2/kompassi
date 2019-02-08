from django.conf import settings
from django.core.management.base import BaseCommand

from oauth2_provider.models import Application

from core.models import Person


class Command(BaseCommand):
    def handle(*args, **options):
        if settings.DEBUG:
            person, unused = Person.get_or_create_dummy()

            Application.objects.get_or_create(
                client_id='kompassi_insecure_test_client_id',
                defaults=dict(
                    user=person.user,
                    redirect_uris='\n'.join([
                        'http://ssoexample.dev:8001/oauth2/callback',
                        'http://infokala.dev:8001/oauth2/callback',
                        'http://tracontent.dev:8001/oauth2/callback',
                    ]),
                    client_type='confidential', # hah
                    authorization_grant_type='authorization-code',
                    client_secret='kompassi_insecure_test_client_secret',
                    name='Insecure test application',
                )
            )
