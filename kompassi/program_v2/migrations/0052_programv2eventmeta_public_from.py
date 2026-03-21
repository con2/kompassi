from django.db import migrations, models
from django.utils.timezone import now


def set_public_from_for_existing_events(apps, schema_editor):
    """
    Preserve all-public behaviour for events that existed before this migration.
    New events start with public_from=None (schedule not public by default).
    """
    ProgramV2EventMeta = apps.get_model("program_v2", "ProgramV2EventMeta")
    ProgramV2EventMeta.objects.update(public_from=now())


class Migration(migrations.Migration):
    dependencies = [
        ("program_v2", "0051_scheduleitem_paikkala_icon"),
    ]

    operations = [
        migrations.AddField(
            model_name="programv2eventmeta",
            name="public_from",
            field=models.DateTimeField(
                blank=True,
                null=True,
                help_text=(
                    "When set to a past datetime, the program schedule is publicly visible. "
                    "Unset or future datetime means the schedule is not public."
                ),
            ),
        ),
        migrations.RunPython(
            set_public_from_for_existing_events,
            reverse_code=migrations.RunPython.noop,
        ),
    ]
