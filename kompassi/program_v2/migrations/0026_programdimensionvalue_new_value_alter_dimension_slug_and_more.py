import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


def populate_program_dimension_value_new_value(apps, schema_editor):
    ProgramDimensionValue = apps.get_model("program_v2", "ProgramDimensionValue")
    DimensionValue = apps.get_model("dimensions", "DimensionValue")

    bulk_update = []
    for pdv in ProgramDimensionValue.objects.all():
        pdv.new_value = DimensionValue.objects.get(
            dimension__universe__scope__slug=pdv.program.event.slug,
            dimension__universe__slug="default",
            dimension__universe__app="program_v2",
            dimension__slug=pdv.dimension.slug,
            slug=pdv.value.slug,
        )
        bulk_update.append(pdv)
    ProgramDimensionValue.objects.bulk_update(bulk_update, ["new_value"], batch_size=400)


class Migration(migrations.Migration):
    dependencies = [
        ("dimensions", "0002_populate"),
        ("program_v2", "0025_scheduleitem_created_at_scheduleitem_updated_at"),
    ]

    operations = [
        migrations.AddField(
            model_name="programdimensionvalue",
            name="new_value",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="+",
                to="dimensions.dimensionvalue",
            ),
        ),
        migrations.AlterField(
            model_name="dimension",
            name="slug",
            field=models.CharField(
                max_length=255,
                validators=[
                    django.core.validators.RegexValidator(
                        message="Tekninen nimi saa sisältää vain pieniä kirjaimia, numeroita sekä väliviivoja.",
                        regex="^[a-z0-9-]+$",
                    )
                ],
            ),
        ),
        migrations.AlterField(
            model_name="dimensionvalue",
            name="slug",
            field=models.CharField(
                max_length=255,
                validators=[
                    django.core.validators.RegexValidator(
                        message="Tekninen nimi saa sisältää vain pieniä kirjaimia, numeroita sekä väliviivoja.",
                        regex="^[a-z0-9-]+$",
                    )
                ],
            ),
        ),
        migrations.AlterField(
            model_name="offerform",
            name="slug",
            field=models.CharField(
                help_text='Tekninen nimi eli "slug" näkyy URL-osoitteissa. Sallittuja merkkejä ovat pienet kirjaimet, numerot ja väliviiva. Teknistä nimeä ei voi muuttaa luomisen jälkeen.',
                max_length=255,
                validators=[
                    django.core.validators.RegexValidator(
                        message="Tekninen nimi saa sisältää vain pieniä kirjaimia, numeroita sekä väliviivoja.",
                        regex="^[a-z0-9-]+$",
                    )
                ],
                verbose_name="Tekninen nimi",
            ),
        ),
        migrations.AlterField(
            model_name="program",
            name="slug",
            field=models.CharField(
                max_length=1023,
                validators=[
                    django.core.validators.RegexValidator(
                        message="Tekninen nimi saa sisältää vain pieniä kirjaimia, numeroita sekä väliviivoja.",
                        regex="^[a-z0-9-]+$",
                    )
                ],
            ),
        ),
        migrations.AlterField(
            model_name="scheduleitem",
            name="slug",
            field=models.CharField(
                help_text="NOTE: Slug must be unique within Event. It does not suffice to be unique within Program.",
                max_length=255,
                validators=[
                    django.core.validators.RegexValidator(
                        message="Tekninen nimi saa sisältää vain pieniä kirjaimia, numeroita sekä väliviivoja.",
                        regex="^[a-z0-9-]+$",
                    )
                ],
                verbose_name="Slug",
            ),
        ),
        migrations.RunPython(
            populate_program_dimension_value_new_value,
            reverse_code=migrations.RunPython.noop,
            elidable=True,
        ),
    ]
