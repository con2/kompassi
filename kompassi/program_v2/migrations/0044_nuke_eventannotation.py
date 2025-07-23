from django.contrib.postgres.fields import ArrayField
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("program_v2", "0043_remove_eventannotation_id_and_more"),
    ]

    operations = [
        migrations.DeleteModel(
            name="EventAnnotation",
        ),
        migrations.CreateModel(
            name="EventAnnotation",
            fields=[
                (
                    "pk",
                    models.CompositePrimaryKey(
                        "meta", "annotation", blank=True, editable=False, primary_key=True, serialize=False
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=True, help_text="If false, this annotation will not be used in this event."
                    ),
                ),
                (
                    "program_form_fields",
                    ArrayField(
                        base_field=models.TextField(),
                        blank=True,
                        default=list,
                        help_text="List of program form field slugs this annotation will be attempted to be extracted from, in order.",
                        size=None,
                    ),
                ),
                (
                    "annotation",
                    models.ForeignKey(
                        on_delete=models.CASCADE,
                        related_name="all_event_annotations",
                        to="program_v2.annotation",
                    ),
                ),
                (
                    "meta",
                    models.ForeignKey(
                        on_delete=models.CASCADE,
                        related_name="all_event_annotations",
                        to="program_v2.programv2eventmeta",
                    ),
                ),
            ],
        ),
    ]
