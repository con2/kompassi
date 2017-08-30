from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models import Q

from badges.models import Badge, BadgesEventMeta


class Command(BaseCommand):
    args = ''
    help = 'Part of the Fuzzy Reissuance Hack. Rescues badges that were wrongly revoked.'

    def add_arguments(self, parser):
        parser.add_argument(
            'event_slugs',
            nargs='+',
            metavar='EVENT_SLUG',
        )

    def handle(self, *args, **options):
        event_slugs = options['event_slugs']

        # please only use with the fuzzy reissuance hack
        for event_slug in event_slugs:
            BadgesEventMeta.objects.get(
                event__slug=event_slug,
                is_using_fuzzy_reissuance_hack=True,
            )

        # the purpose is to reduce the amount of badges to print
        with transaction.atomic():
            for candidate_badge in Badge.objects.filter(
                personnel_class__event__slug__in=event_slugs,

                # is not printed
                printed_separately_at__isnull=True,
                batch__printed_at__isnull=True,

                # is not revoked
                revoked_at__isnull=True,

                # is managed
                person__isnull=False,
            ):
                # is printed
                q = Q(printed_separately_at__isnull=False) | Q(batch__printed_at__isnull=False)

                q &= Q(
                    # matches the same basic info
                    personnel_class=candidate_badge.personnel_class,
                    person=candidate_badge.person,
                    first_name=candidate_badge.first_name,
                    surname=candidate_badge.surname,
                    nick=candidate_badge.nick,
                    job_title=candidate_badge.job_title,

                    # is revoked
                    revoked_at__isnull=False
                )

                badge_to_restore = Badge.objects.filter(q).order_by('-id').first()

                if badge_to_restore:
                    badge_to_restore.unrevoke()
                    candidate_badge.revoke()
                    print('+', end='')
                else:
                    print('.', end='')

        print()
