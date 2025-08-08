from django.core.management.base import BaseCommand

from kompassi.dimensions.models.annotation_dto import AnnotationDTO
from kompassi.dimensions.models.scope import Scope

from ...emperkelators.tracon2025 import TraconEmperkelator
from ...models.registry import Registry


class Command(BaseCommand):
    help = "Setup the involvement app by creating the necessary scopes and registries."

    def handle(self, *args, **options):
        Registry.objects.update_or_create(
            scope=Scope.get_root_scope(),
            slug="users",
            defaults=dict(
                title_fi="Kompassin käyttäjärekisteri",
                title_en="Users of Kompassi",
                title_sv="Användare av Kompassi",
                policy_url_fi="https://ry.tracon.fi/tietosuoja/rekisteriselosteet/kompassi",
            ),
        )

        AnnotationDTO.save_many(TraconEmperkelator.get_annotation_dtos())
