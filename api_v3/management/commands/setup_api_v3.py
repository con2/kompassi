from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Set up API v3'

    def handle(self, *args, **options):
        if settings.DEBUG:
            from oauth2_provider.models import Application
            Application.objects.get_or_create(
                name='Kompassi2 DEV',
                defaults=dict(
                    client_id='insecure kompassi v2 development client id',
                    client_secret='',
                    client_type='public',
                    authorization_grant_type='implicit',
                    skip_authorization=True,
                    redirect_uris='http://localhost:3000/oauth2/callback',
                )
            )
