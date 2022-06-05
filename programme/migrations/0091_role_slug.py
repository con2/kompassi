import django.core.validators
from django.db import migrations, models

from core.utils import slugify


def populate_slug(apps, schema_editor):
    role = apps.get_model("programme", "Role")

    for role in role.objects.all():
        role.slug = slugify(role.title)
        role.save()


class Migration(migrations.Migration):

    dependencies = [
        ("programme", "0090_alternativeprogrammeform_role"),
    ]

    operations = [
        migrations.AddField(
            model_name="role",
            name="slug",
            field=models.CharField(
                default="",
                help_text='Tekninen nimi eli "slug" näkyy URL-osoitteissa. Sallittuja merkkejä ovat pienet kirjaimet, numerot ja väliviiva. Teknistä nimeä ei voi muuttaa luomisen jälkeen.',
                max_length=255,
                validators=[
                    django.core.validators.RegexValidator(
                        message="Tekninen nimi saa sisältää vain pieniä kirjaimia, numeroita sekä väliviivoja.",
                        regex="[a-z0-9-]+",
                    )
                ],
                verbose_name="Tekninen nimi",
            ),
            preserve_default=False,
        ),
        migrations.RunPython(populate_slug),
    ]
