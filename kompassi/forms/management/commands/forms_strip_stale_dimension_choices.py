from django.core.management.base import BaseCommand
from django.db import transaction

from ...models.field import FieldType
from ...models.form import Form

DIMENSION_FIELD_TYPES = {field_type.value for field_type in FieldType if field_type.is_dimension_field}


class Command(BaseCommand):
    help = (
        "One-off fix for a bug where the survey editor persisted stale, "
        "possibly mistranslated dimension choices into Form.fields. "
        "Strips choices from dimension fields (they must only ever come "
        "from live enrichment) and refreshes cached_enriched_fields."
    )

    def handle(self, *args, **options):
        updated = 0

        with transaction.atomic():
            for form in Form.objects.select_for_update():
                changed = False
                new_fields = []

                for field in form.fields:
                    if field.get("type") in DIMENSION_FIELD_TYPES and field.get("choices"):
                        field = {key: value for key, value in field.items() if key != "choices"}
                        changed = True
                    new_fields.append(field)

                if changed:
                    form.fields = new_fields
                    form.save(update_fields=["fields", "cached_enriched_fields"])
                    updated += 1

        self.stdout.write(self.style.SUCCESS(f"Stripped stale dimension choices from {updated} form(s)."))
