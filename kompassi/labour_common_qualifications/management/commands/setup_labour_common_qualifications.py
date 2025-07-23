from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand

from kompassi.labour.models import Qualification

from ...models import JVKortti


class Command(BaseCommand):
    args = ""
    help = "Setup common labour qualifications"

    def handle(*args, **options):
        content_type = ContentType.objects.get_for_model(JVKortti)
        Qualification.objects.get_or_create(
            slug="jv-kortti", defaults=dict(name="JV-kortti", qualification_extra_content_type=content_type)
        )

        for slug, name in [
            ("b-ajokortti", "Henkilöauton ajokortti (B)"),
            ("c-ajokortti", "Kuorma-auton ajokortti (C)"),
            ("ea1", "Ensiapukoulutus EA1"),
            ("ea2", "Ensiapukoulutus EA2"),
            ("hygieniapassi", "Hygieniapassi"),
        ]:
            Qualification.objects.get_or_create(slug=slug, defaults=dict(name=name))
