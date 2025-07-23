from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("membership", "0010_remove_membershiporganizationmeta_membership_fee"),
    ]

    operations = [
        migrations.AlterField(
            model_name="membership",
            name="organization",
            field=models.ForeignKey(
                on_delete=models.CASCADE, related_name="memberships", verbose_name="Yhdistys", to="core.Organization"
            ),
            preserve_default=True,
        ),
    ]
