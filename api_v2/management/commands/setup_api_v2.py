# encoding: utf-8

from django.core.management.base import BaseCommand, make_option

from oauth2_provider.models import Application

from core.models import Person


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--test',
            action='store_true',
            dest='test',
            default=False,
            help='Setup api_v2 for testing'
        ),
    )

    def handle(*args, **options):
        if options['test']:
            person, unused = Person.get_or_create_dummy()

            Application.objects.get_or_create(
                client_id='kompassi_insecure_test_client_id',
                user=person.user,
                redirect_uris='http://ssoexample.dev:8001/oauth2/callback',
                client_type='confidential', # hah
                authorization_grant_type='authorization-code',
                client_secret='kompassi_insecure_test_client_secret',
                name='Insecure test application',
            )
