import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


def populate_response_dimension_value_new_value(apps, schema_editor):
    ResponseDimensionValue = apps.get_model("forms", "ResponseDimensionValue")
    DimensionValue = apps.get_model("dimensions", "DimensionValue")

    bulk_update = []
    for rdv in ResponseDimensionValue.objects.all():
        rdv.new_value = DimensionValue.objects.get(
            dimension__universe__scope__slug=rdv.dimension.survey.event.slug,
            dimension__universe__slug=rdv.dimension.survey.slug,
            dimension__universe__app="forms",
            dimension__slug=rdv.dimension.slug,
            slug=rdv.value.slug,
        )
        bulk_update.append(rdv)
    ResponseDimensionValue.objects.bulk_update(bulk_update, ["new_value"], batch_size=400)


class Migration(migrations.Migration):
    dependencies = [
        ("dimensions", "0002_populate"),
        ("forms", "0029_formseventmeta"),
    ]

    operations = [
        migrations.AddField(
            model_name="responsedimensionvalue",
            name="new_value",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="+",
                to="dimensions.dimensionvalue",
            ),
        ),
        migrations.RunPython(
            populate_response_dimension_value_new_value,
            reverse_code=migrations.RunPython.noop,
            elidable=True,
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
            model_name="form",
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
            model_name="survey",
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
    ]
