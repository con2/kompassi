from django.db import migrations, models
from django.db.models import F
from django.db.models.functions import Upper


def uppercase_value_ordering_choices(apps, schema_editor):
    Dimension = apps.get_model("dimensions", "Dimension")
    Dimension.objects.all().update(value_ordering=Upper(F("value_ordering")))


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
            uppercase_value_ordering_choices,
            reverse_code=migrations.RunPython.noop,
            elidable=True,
        ),
    ]
