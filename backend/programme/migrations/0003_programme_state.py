from django.db import migrations, models


def publish_all_existing_programme(apps, schema_editor):
    Programme = apps.get_model("programme", "programme")
    Programme.objects.filter(
        start_time__isnull=False,
        length__isnull=False,
        room__isnull=False,
    ).update(state="published")


class Migration(migrations.Migration):
    dependencies = [
        ("programme", "0002_auto_20150115_1949"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="room",
            name="public",
        ),
        migrations.AddField(
            model_name="programme",
            name="state",
            field=models.CharField(
                default="accepted",
                help_text='Tilassa "Julkaistu" olevat ohjelmat n\xe4kyv\xe4t ohjelmakartassa, jos ohjelmakartta on julkinen.',
                max_length=15,
                verbose_name="Ohjelmanumeron tila",
                choices=[
                    ("idea", "Ideoitu sis\xe4isti"),
                    ("asked", "Kysytty ohjelmanj\xe4rjest\xe4j\xe4lt\xe4"),
                    ("offered", "Ohjelmatarjous vastaanotettu"),
                    ("accepted", "Hyv\xe4ksytty"),
                    ("published", "Julkaistu"),
                    ("cancelled", "Peruutettu"),
                    ("rejected", "Hyl\xe4tty"),
                ],
            ),
            preserve_default=True,
        ),
        migrations.RunPython(publish_all_existing_programme, elidable=True),
    ]
