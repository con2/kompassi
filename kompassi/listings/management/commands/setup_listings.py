from django.core.management.base import BaseCommand


class Command(BaseCommand):
    args = ""
    help = "Create default listings and add events to them"

    def handle(*args, **opts):
        from kompassi.core.models import Event

        from ...models import ExternalEvent, Listing

        # Hide ExternalEvents for which there is an actual Event counterpart
        ExternalEvent.objects.filter(
            slug__in=Event.objects.filter(public=True).values_list("slug", flat=True),
        ).update(
            public=False,
        )

        # Setup default listings
        for hostname, title, description in [
            (
                "animecon.fi",
                "Suomen animetapahtumat",
                "HUOM! Animecon.fi-listaus on poistettu käytöstä. Katso osoite conit.fi.",
            ),
            (
                "conit.fi",
                "Suomen conitapahtumat",
                (
                    "Tämä on listaus Suomessa järjestettävistä conitapahtumista. "
                    "Listaukseen lisätään kaikki voittoa tavoittelemattomalta pohjalta "
                    "vapaaehtoisvoimin järjestettävät conitapahtumat sitä mukaa kun ne "
                    "tulevat ylläpitäjän tietoon."
                ),
            ),
        ]:
            listing, created = Listing.objects.get_or_create(
                hostname=hostname,
                defaults=dict(
                    title=title,
                    description=description,
                ),
            )
