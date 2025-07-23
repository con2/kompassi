from collections import defaultdict

import django.db.models.deletion
from django.db import migrations, models


def populate_survey_default_dimensions(apps, schema_editor):
    Scope = apps.get_model("dimensions", "Scope")
    Universe = apps.get_model("dimensions", "Universe")
    DimensionValue = apps.get_model("dimensions", "DimensionValue")
    Survey = apps.get_model("forms", "Survey")
    SurveyDefaultDimensionValue = apps.get_model("forms", "SurveyDefaultDimensionValue")

    for survey in Survey.objects.all():
        scope = Scope.objects.get(event=survey.event)
        try:
            if survey.app == "forms":
                universe = Universe.objects.get(scope=scope, slug=survey.slug, app="forms")
            else:
                universe = Universe.objects.get(scope=scope, app="program_v2")
        except Universe.DoesNotExist:
            # ei universumii, ei ongelmii
            continue

        cached_default_dimensions: defaultdict[str, set[str]] = defaultdict(set)
        for dimension_value in DimensionValue.objects.filter(dimension__universe=universe, is_initial=True):
            SurveyDefaultDimensionValue.objects.get_or_create(survey=survey, value=dimension_value)
            cached_default_dimensions[dimension_value.dimension.slug].add(dimension_value.slug)

        survey.cached_default_dimensions = {k: list(v) for k, v in cached_default_dimensions.items()}
        survey.save(update_fields=["cached_default_dimensions"])


class Migration(migrations.Migration):
    dependencies = [
        ("dimensions", "0008_alter_dimension_slug_alter_dimensionvalue_slug"),
        ("forms", "0038_survey_created_at_survey_created_by_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="survey",
            name="cached_default_dimensions",
            field=models.JSONField(blank=True, default=dict),
        ),
        migrations.CreateModel(
            name="SurveyDefaultDimensionValue",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "survey",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="default_dimensions",
                        to="forms.survey",
                    ),
                ),
                (
                    "value",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, related_name="+", to="dimensions.dimensionvalue"
                    ),
                ),
            ],
            options={
                "unique_together": {("survey", "value")},
            },
        ),
        migrations.RunPython(
            populate_survey_default_dimensions,
            migrations.RunPython.noop,
            elidable=True,
        ),
    ]
