# encoding: utf-8

from django.core.management import call_command
from django.core.management.base import BaseCommand, make_option

import subprocess


class Command(BaseCommand):
    def handle(*args, **opts):
        subprocess.call(['behave', '-t', '~@fullstack', '-t', '~@wip'])