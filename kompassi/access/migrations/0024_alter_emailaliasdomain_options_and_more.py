import django.db.models.deletion
from django.db import migrations, models


def populate_variant(app_config, schema_editor):
    EmailAliasType = app_config.get_model("access", "EmailAliasType")
    for alias_type in EmailAliasType.objects.all():
        match alias_type.account_name_code:
            case "organizations.tracon_ry.email_aliases:nick":
                variant_slug = "CUSTOM"
            case "access.email_aliases:nick":
                variant_slug = "NICK"
            case "access.email_aliases:firstname_surname":
                variant_slug = "FIRSTNAME_LASTNAME"
            case "organizations.kotae_ry.email_aliases:nick":
                variant_slug = "NICK"
            case other:
                raise NotImplementedError(other)
        alias_type.variant_slug = variant_slug
        alias_type.save()


class Migration(migrations.Migration):
    dependencies = [
        ("access", "0023_alter_privilege_slug"),
        ("core", "0043_emailverificationtoken_language_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="emailaliasdomain",
            options={},
        ),
        migrations.AlterModelOptions(
            name="emailaliastype",
            options={},
        ),
        migrations.AddField(
            model_name="emailaliastype",
            name="variant_slug",
            field=models.CharField(
                blank=True,
                choices=[("FIRSTNAME_LASTNAME", "firstname.lastname"), ("NICK", "nick"), ("CUSTOM", "custom")],
                default="",
                max_length=18,
            ),
        ),
        migrations.AlterField(
            model_name="emailaliasdomain",
            name="domain_name",
            field=models.CharField(
                help_text="eg. example.com",
                max_length=255,
                unique=True,
            ),
        ),
        migrations.AlterField(
            model_name="emailaliasdomain",
            name="organization",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="core.organization",
            ),
        ),
        migrations.RunPython(
            populate_variant,
            reverse_code=migrations.RunPython.noop,
            elidable=True,
        ),
    ]
