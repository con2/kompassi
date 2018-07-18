from functools import reduce

from django.core.management.base import BaseCommand
from django.db.models import Q
from django.utils.timezone import now


class Command(BaseCommand):
    args = ''
    help = 'Create default listings and add events to them'

    def handle(*args, **opts):
        from core.models import Event
        from ...models import Listing, ExternalEvent

        # Hide ExternalEvents for which there is an actual Event counterpart
        ExternalEvent.objects.filter(
            slug__in=Event.objects.filter(public=True).values_list('slug', flat=True),
        ).update(
            public=False,
        )

        # Setup default listings
        for hostname, title, description, keywords, exclude_keywords in [
            ('animecon.fi', 'Suomen animetapahtumat', (
                'Tämä on listaus Suomessa järjestettävistä animetapahtumista. '
                'Listaukseen lisätään kaikki voittoa tavoittelemattomalta pohjalta '
                'vapaaehtoisvoimin järjestettävät animetapahtumat sitä mukaa kun ne '
                'tulevat ylläpitäjän tietoon.'
            ), (
                'desucon',
                'hypecon',
                'kawacon',
                'lakeuscon',
                'matsucon',
                'mimicon',
                'nekocon',
                'nippori',
                'tracon',
                'yukicon',
            ), (
                'hitpoint',
            )),
            ('conit.fi', 'Suomen conitapahtumat', (
                'Tämä on listaus Suomessa järjestettävistä conitapahtumista. '
                'Listaukseen lisätään kaikki voittoa tavoittelemattomalta pohjalta '
                'vapaaehtoisvoimin järjestettävät conitapahtumat sitä mukaa kun ne '
                'tulevat ylläpitäjän tietoon.'
            ), (
                'aicon',
                'desucon',
                'finncon',
                'hellocon',
                'hypecon',
                'kawacon',
                'lakeuscon',
                'matsucon',
                'mimicon',
                'nekocon',
                'nippori',
                'popcult',
                'ropecon',
                'tampere kuplii',
                'tracon',
                'yukicon',
            ), (
                'nights',
            )),
        ]:
            listing, created = Listing.objects.get_or_create(
                hostname=hostname,
                defaults=dict(
                    title=title,
                    description=description,
                ),
            )

            def raeducci(keywords):
                """
                Given a list of keywords, returns a Q that matches objects that have any of those
                keywords contained in their `name` attribute case-insensitively.
                """
                keywords = list(keywords)
                return reduce((lambda q, k: q | Q(name__icontains=k)), keywords, Q(name__icontains=keywords.pop()))

            q = Q(public=True) & raeducci(keywords)

            if exclude_keywords:
                q = q & ~raeducci(exclude_keywords)

            events = Event.objects.filter(q)
            print('events', events)
            external_events = ExternalEvent.objects.filter(q)

            listing.events.set(events)
            listing.external_events.set(external_events)

