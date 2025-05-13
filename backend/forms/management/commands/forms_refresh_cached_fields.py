from django.core.management.base import BaseCommand

from ...models.form import Form
from ...models.response import Response
from ...models.survey import Survey


class Command(BaseCommand):
    help = "Refreshes enriched_fields for all forms"

    def handle(self, *args, **options):
        Survey.refresh_cached_default_dimensions_qs(Survey.objects.all())
        Form.refresh_enriched_fields_qs(Form.objects.all())
        Response.refresh_cached_fields_qs(Response.objects.all())
