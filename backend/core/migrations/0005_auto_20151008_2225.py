from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0004_organization"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="organization",
            options={"verbose_name": "Organisaatio", "verbose_name_plural": "Organisaatiot"},
        ),
        migrations.RemoveField(
            model_name="event",
            name="organization_name",
        ),
        migrations.RemoveField(
            model_name="event",
            name="organization_url",
        ),
        migrations.AlterField(
            model_name="event",
            name="organization",
            field=models.ForeignKey(
                on_delete=models.CASCADE, default=1, verbose_name="J\xe4rjest\xe4j\xe4taho", to="core.Organization"
            ),
            preserve_default=False,
        ),
    ]
