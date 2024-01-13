from django.conf import settings
from django.db import migrations, models


def populate_members_group(apps, schema_editor):
    Group = apps.get_model("auth", "group")
    MembershipOrganizationMeta = apps.get_model("membership", "membershiporganizationmeta")

    for meta in MembershipOrganizationMeta.objects.all():
        group_name = "{installation_slug}-{host_slug}-{app_label}-{suffix}".format(
            installation_slug=settings.KOMPASSI_INSTALLATION_SLUG,
            host_slug=meta.organization.slug,
            app_label="membership",
            suffix="members",
        )

        group, created = Group.objects.get_or_create(name=group_name)

        meta.members_group = group
        meta.save()


class Migration(migrations.Migration):
    dependencies = [
        ("auth", "0001_initial"),
        ("membership", "0011_auto_20151020_0016"),
    ]

    operations = [
        migrations.AddField(
            model_name="membershiporganizationmeta",
            name="members_group",
            field=models.ForeignKey(
                on_delete=models.CASCADE,
                related_name="members_group_for",
                verbose_name="J\xe4senryhm\xe4",
                blank=True,
                to="auth.Group",
                null=True,
            ),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name="membershiporganizationmeta",
            name="admin_group",
            field=models.ForeignKey(
                on_delete=models.CASCADE,
                related_name="admin_group_for",
                verbose_name="Yll\xe4pit\xe4j\xe4ryhm\xe4",
                to="auth.Group",
            ),
            preserve_default=True,
        ),
        migrations.RunPython(populate_members_group, elidable=True),
        migrations.AlterField(
            model_name="membershiporganizationmeta",
            name="members_group",
            field=models.ForeignKey(
                on_delete=models.CASCADE,
                related_name="members_group_for",
                verbose_name="J\xe4senryhm\xe4",
                to="auth.Group",
            ),
            preserve_default=True,
        ),
    ]
