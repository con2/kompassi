import django.core.validators
from django.db import migrations, models

from kompassi.core.utils import slugify


def populate_room_slug(apps, schema_editor):
    Room = apps.get_model("programme", "room")
    for room in Room.objects.all():
        room.slug = slugify(room.name)
        room.save()


class Migration(migrations.Migration):
    dependencies = [
        ("programme", "0005_programme_end_time"),
    ]

    operations = [
        migrations.AddField(
            model_name="room",
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
            name="room",
            unique_together={("venue", "order"), ("venue", "slug")},
        ),
        migrations.RunPython(populate_room_slug, elidable=True),
    ]
