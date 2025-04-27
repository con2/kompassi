from django.core.management.base import BaseCommand

from ...models.form import Form


class Command(BaseCommand):
    help = "Refreshes enriched_fields for all forms"

    def handle(self, *args, **options):
        Form.refresh_enriched_fields_qs(Form.objects.all())
