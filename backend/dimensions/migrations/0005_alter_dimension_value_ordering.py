from django.db import migrations, models


def emsensiblen_value_ordering(s: str):
    match s.upper():
        case "1" | "MANUAL":
            return "MANUAL"
        case "2" | "SLUG":
            return "SLUG"
        case "3" | "TITLE":
            return "TITLE"
        case _:
            return "SLUG"


def wtfix_value_ordering(apps, schema_editor):
    Dimension = apps.get_model("dimensions", "Dimension")
    bulk_update = []
    for dimension in Dimension.objects.all():
        dimension.value_ordering = emsensiblen_value_ordering(dimension.value_ordering)
        bulk_update.append(dimension)
    Dimension.objects.bulk_update(bulk_update, fields=["value_ordering"], batch_size=400)


class Migration(migrations.Migration):
    dependencies = [
        ("dimensions", "0004_alter_universe_unique_together"),
    ]

    operations = [
        migrations.AlterField(
            model_name="dimension",
            name="value_ordering",
            field=models.CharField(
                choices=[
                    ("MANUAL", "Manual"),
                    ("SLUG", "Alphabetical (slug)"),
                    ("TITLE", "Alphabetical (localized title)"),
                ],
                default="TITLE",
                help_text="In which order are the values of this dimension returned in the GraphQL API. NOTE: When using Alphabetical (localized title), the language needs to be provided to `values` and `values.title` fields separately.",
                max_length=6,
            ),
        ),
        migrations.RunPython(
            wtfix_value_ordering,
            reverse_code=migrations.RunPython.noop,
            elidable=True,
        ),
    ]
