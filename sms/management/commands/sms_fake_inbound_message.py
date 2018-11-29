# encoding: utf-8

from django.core.management.base import BaseCommand

# from sms.utils import fake_inbound_message


class Command(BaseCommand):
    def handle(*args, **opts):
        # fake_inbound_message(
        #     sender=args[1],
        #     message=args[2],
        # )
        raise NotImplementedError()
