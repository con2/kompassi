import django.db.models.deletion
from django.db import migrations, models


def populate_survey_universe(apps, schema_editor):
    Scope = apps.get_model("dimensions", "Scope")
    Survey = apps.get_model("forms", "Survey")
    Universe = apps.get_model("dimensions", "Universe")

    for survey in Survey.objects.all():
        scope = Scope.objects.get_or_create(
            event=survey.event,
            defaults=dict(
                slug=survey.event.slug,
                name=survey.event.name,
                organization=survey.event.organization,
            ),
        )[0]

        match survey.app_name:
            case "forms":
                # mirror Survey._get_universe
                survey.universe = Universe.objects.get_or_create(
                    scope=scope,
                    slug=survey.slug,
                    app="forms",
                )[0]
            case "program_v2":
                # mirror get_program_universe
                survey.universe = Universe.objects.get_or_create(
                    scope=scope,
                    slug="program",
                    app="program_v2",
                )[0]
            case _:
                raise NotImplementedError(survey.app)

        survey.save(update_fields=["universe"])


class Migration(migrations.Migration):
    dependencies = [
        ("dimensions", "0011_dimensionvalue_is_subject_locked"),
        ("forms", "0046_rename_response_responsedimensionvalue_subject_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="survey",
            name="universe",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="surveys",
                to="dimensions.universe",
            ),
        ),
        migrations.RunPython(
            populate_survey_universe,
            migrations.RunPython.noop,
            elidable=True,
        ),
    ]
