from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("programme", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="programmeeventmeta",
            name="public",
        ),
        migrations.AddField(
            model_name="programmeeventmeta",
            name="public_from",
            field=models.DateTimeField(
                help_text="Ohjelmakartta n\xe4kyy kansalle t\xe4st\xe4 eteenp\xe4in.",
                null=True,
                verbose_name="Ohjelmakartan julkaisuaika",
                blank=True,
            ),
            preserve_default=True,
        ),
    ]
