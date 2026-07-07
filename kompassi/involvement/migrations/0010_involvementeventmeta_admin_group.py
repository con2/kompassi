import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


def create_admin_groups(apps, schema_editor):
    InvolvementEventMeta = apps.get_model("involvement", "InvolvementEventMeta")
    Group = apps.get_model("auth", "Group")

    for meta in InvolvementEventMeta.objects.select_related("event").all():
        # Mirrors GroupManagementMixin.make_group_name for app_label "involvement".
        group_name = f"{settings.KOMPASSI_INSTALLATION_SLUG}-{meta.event.slug}-involvement-admins"
        group, _ = Group.objects.get_or_create(name=group_name)
        meta.admin_group = group
        meta.save(update_fields=["admin_group"])


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
        ("involvement", "0009_involvementeventmeta_shirts_frozen_at"),
    ]

    operations = [
        migrations.AddField(
            model_name="involvementeventmeta",
            name="admin_group",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="+",
                to="auth.group",
            ),
        ),
        migrations.RunPython(create_admin_groups, noop),
        migrations.AlterField(
            model_name="involvementeventmeta",
            name="admin_group",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="+",
                to="auth.group",
            ),
        ),
    ]
