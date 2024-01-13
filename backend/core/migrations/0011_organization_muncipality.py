from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0010_organization_public"),
    ]

    operations = [
        migrations.AddField(
            model_name="organization",
            name="muncipality",
            field=models.CharField(
                help_text="Kunta, johon yhdistys on rekister\xf6ity.",
                max_length=127,
                verbose_name="Yhdistyksen kotipaikka",
                blank=True,
            ),
            preserve_default=True,
        ),
    ]
