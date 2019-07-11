
from django.core.management.base import BaseCommand, CommandError
from django.core.mail import send_mail
from django.template.loader import render_to_string

from ...proxies import SignupExtraV2AfterpartyProxy

class Command(BaseCommand):
    help = 'Sends afterparty info mail'

    def add_arguments(self, parser):
        parser.add_argument('--really', default=False, action='store_true')

    def handle(self, *args, **options):
        really = options['really']
        signup_extras = SignupExtraV2AfterpartyProxy.objects.filter(afterparty_participation=True)

        for signup_extra in signup_extras:
            vars = dict(signup_extra=signup_extra)
            subject = 'Tracon (2016): Tervetuloa kaatajaisiin!'
            sender = 'tracon11-kaatajaiset@kompassi.eu'
            recipient = signup_extra.person.name_and_email
            body = render_to_string('tracon11_afterparty_message.eml', vars)

            if really:
                send_mail(
                    subject,
                    body,
                    sender,
                    [recipient],
                    fail_silently=False
                )
                print(recipient)
            else:
                print('To:', recipient)
                print('Subject:', subject)
                print()
                print(body)
                print()
                print()
