import django.contrib.postgres.indexes
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


def populate_annotations(apps, schema_editor):
    """
    Populate the `annotations` field for existing ScheduleItems.
    This is a placeholder function that can be modified to set specific annotations.
    """
    ScheduleItem = apps.get_model("program_v2", "ScheduleItem")
    for item in ScheduleItem.objects.all().exclude(subtitle=""):
        item.annotations = {"internal:subtitle": item.subtitle}
        item.save(update_fields=["annotations"])


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0043_emailverificationtoken_language_and_more"),
        ("dimensions", "0011_dimensionvalue_is_subject_locked"),
        ("forms", "0046_rename_response_responsedimensionvalue_subject_and_more"),
        ("program_v2", "0039_programv2eventmeta_default_registry"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="scheduleitem",
            name="annotations",
            field=models.JSONField(blank=True, default=dict),
        ),
        migrations.RunPython(
            populate_annotations,
            reverse_code=migrations.RunPython.noop,
            elidable=True,
        ),
        migrations.CreateModel(
            name="ScheduleItemDimensionValue",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
            ],
            options={
                "ordering": ("value__dimension__order", "value__order"),
            },
        ),
        migrations.RenameField(
            model_name="programdimensionvalue",
            old_name="program",
            new_name="subject",
        ),
        migrations.RenameField(
            model_name="scheduleitem",
            old_name="length",
            new_name="duration",
        ),
        migrations.RemoveField(
            model_name="program",
            name="cached_location",
        ),
        migrations.RemoveField(
            model_name="scheduleitem",
            name="subtitle",
        ),
        migrations.AddField(
            model_name="program",
            name="cached_combined_dimensions",
            field=models.JSONField(blank=True, default=dict),
        ),
        migrations.AddField(
            model_name="scheduleitem",
            name="cached_combined_dimensions",
            field=models.JSONField(blank=True, default=dict),
        ),
        migrations.AddField(
            model_name="scheduleitem",
            name="cached_dimensions",
            field=models.JSONField(blank=True, default=dict),
        ),
        migrations.AlterUniqueTogether(
            name="programdimensionvalue",
            unique_together={("subject", "value")},
        ),
        migrations.AddIndex(
            model_name="program",
            index=django.contrib.postgres.indexes.GinIndex(
                fields=["cached_combined_dimensions"],
                name="program_v2_program_gin",
                opclasses=["jsonb_path_ops"],
            ),
        ),
        migrations.AddIndex(
            model_name="scheduleitem",
            index=django.contrib.postgres.indexes.GinIndex(
                fields=["cached_combined_dimensions"],
                name="program_v2_scheduleitem_gin",
                opclasses=["jsonb_path_ops"],
            ),
        ),
        migrations.AddField(
            model_name="scheduleitemdimensionvalue",
            name="subject",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="dimensions",
                to="program_v2.scheduleitem",
            ),
        ),
        migrations.AddField(
            model_name="scheduleitemdimensionvalue",
            name="value",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="+",
                to="dimensions.dimensionvalue",
            ),
        ),
        migrations.AlterUniqueTogether(
            name="scheduleitemdimensionvalue",
            unique_together={("subject", "value")},
        ),
    ]
