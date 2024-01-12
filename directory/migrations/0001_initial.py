# Generated by Django 1.10.7 on 2017-07-30 09:33
import core.models.group_management_mixin
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("auth", "0008_alter_user_username_max_length"),
        ("core", "0027_event_panel_css_class"),
    ]

    operations = [
        migrations.CreateModel(
            name="DirectoryAccessGroup",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("active_from", models.DateTimeField(blank=True, null=True)),
                ("active_until", models.DateTimeField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("group", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="auth.Group")),
            ],
            options={
                "verbose_name": "directory access group",
                "verbose_name_plural": "directory access groups",
                "ordering": ("organization", "group"),
            },
        ),
        migrations.CreateModel(
            name="DirectoryOrganizationMeta",
            fields=[
                (
                    "organization",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        primary_key=True,
                        serialize=False,
                        to="core.Organization",
                        verbose_name="organization",
                    ),
                ),
            ],
            bases=(models.Model, core.models.group_management_mixin.GroupManagementMixin),
        ),
        migrations.AddField(
            model_name="directoryaccessgroup",
            name="organization",
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="core.Organization"),
        ),
    ]
