import django.db.models.deletion
from django.db import migrations, models


def clear_existing_internal_aliases(apps, schema_editor):
    InternalEmailAlias = apps.get_model("access", "InternalEmailAlias")
    InternalEmailAlias.objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [
        ("access", "0026_alter_privilege_options_remove_privilege_grant_code_and_more"),
    ]

    operations = [
        migrations.RunPython(
            clear_existing_internal_aliases,
            reverse_code=migrations.RunPython.noop,
            elidable=True,
        ),
        migrations.AlterModelOptions(
            name="internalemailalias",
            options={},
        ),
        migrations.AlterField(
            model_name="internalemailalias",
            name="account_name",
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name="internalemailalias",
            name="created_at",
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name="internalemailalias",
            name="domain",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="access.emailaliasdomain",
            ),
        ),
        migrations.AlterField(
            model_name="internalemailalias",
            name="email_address",
            field=models.CharField(
                help_text="denormalized for search, computed automatically",
                max_length=511,
            ),
        ),
        migrations.AlterField(
            model_name="internalemailalias",
            name="modified_at",
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name="internalemailalias",
            name="target_emails",
            field=models.TextField(
                help_text="plain addresses separated by whitespace",
                verbose_name="target e-mail addresses",
            ),
        ),
        migrations.AlterUniqueTogether(
            name="internalemailalias",
            unique_together={("domain", "account_name")},
        ),
    ]
