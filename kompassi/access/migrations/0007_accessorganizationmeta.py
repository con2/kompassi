from django.db import migrations, models

import kompassi.core.models.group_management_mixin


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0016_person_allow_work_history_sharing"),
        ("auth", "0001_initial"),
        ("access", "0006_group_grant_active_until"),
    ]

    operations = [
        migrations.CreateModel(
            name="AccessOrganizationMeta",
            fields=[
                (
                    "organization",
                    models.OneToOneField(
                        on_delete=models.CASCADE,
                        primary_key=True,
                        serialize=False,
                        to="core.Organization",
                        verbose_name="Organisaatio",
                    ),
                ),
                (
                    "admin_group",
                    models.ForeignKey(
                        on_delete=models.CASCADE, verbose_name="Yll\xe4pit\xe4j\xe4ryhm\xe4", to="auth.Group"
                    ),
                ),
            ],
            options={
                "verbose_name": "P\xe4\xe4synvalvonnan asetukset",
            },
            bases=(models.Model, kompassi.core.models.group_management_mixin.GroupManagementMixin),
        ),
    ]
