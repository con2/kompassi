from django.db import migrations


def delete_inactive_involvements(apps, schema_editor):
    """
    TODO(#728): Soft delete of program hosts
    Removing a program host was soft delete via is_active=False
    for a while. But we can't distinguish soft deleted
    program hosts from cancelled programs using is_active alone.
    So we are now hard deleting program hosts instead.
    """
    Involvement = apps.get_model("involvement", "Involvement")
    Involvement.objects.filter(
        is_active=False,
        program__isnull=False,
    ).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("program_v2", "0040_scheduleitemdimensionvalue_and_more"),
    ]

    operations = [
        migrations.RunPython(
            delete_inactive_involvements,
            reverse_code=migrations.RunPython.noop,
            elidable=True,
        )
    ]
