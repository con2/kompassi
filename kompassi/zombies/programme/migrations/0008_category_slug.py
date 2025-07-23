import django.core.validators
from django.db import migrations, models

from kompassi.core.utils import slugify


def populate_slug(apps, schema_editor):
    Category = apps.get_model("programme", "category")

    for category in Category.objects.all():
        category.slug = slugify(category.title)
        category.save()


class Migration(migrations.Migration):
    dependencies = [
        ("programme", "0007_room_slug_not_null"),
    ]

    operations = [
        migrations.AddField(
            model_name="category",
            name="slug",
            field=models.CharField(
                validators=[
                    django.core.validators.RegexValidator(
                        regex="[a-z0-9-]+",
                        message="Tekninen nimi saa sis\xe4lt\xe4\xe4 vain pieni\xe4 kirjaimia, numeroita sek\xe4 v\xe4liviivoja.",
                    )
                ],
                max_length=63,
                blank=True,
                help_text='Tekninen nimi eli "slug" n\xe4kyy URL-osoitteissa. Sallittuja merkkej\xe4 ovat pienet kirjaimet, numerot ja v\xe4liviiva. Teknist\xe4 nime\xe4 ei voi muuttaa luomisen j\xe4lkeen.',
                null=True,
                verbose_name="Tekninen nimi",
            ),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name="category",
            unique_together={("event", "slug")},
        ),
        migrations.RunPython(populate_slug, elidable=True),
        migrations.AlterField(
            model_name="category",
            name="slug",
            field=models.CharField(
                help_text='Tekninen nimi eli "slug" n\xe4kyy URL-osoitteissa. Sallittuja merkkej\xe4 ovat pienet kirjaimet, numerot ja v\xe4liviiva. Teknist\xe4 nime\xe4 ei voi muuttaa luomisen j\xe4lkeen.',
                max_length=63,
                verbose_name="Tekninen nimi",
                validators=[
                    django.core.validators.RegexValidator(
                        regex="[a-z0-9-]+",
                        message="Tekninen nimi saa sis\xe4lt\xe4\xe4 vain pieni\xe4 kirjaimia, numeroita sek\xe4 v\xe4liviivoja.",
                    )
                ],
            ),
            preserve_default=True,
        ),
    ]
