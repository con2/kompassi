from django.db import migrations


def clear_subset_values(apps, schema_editor):
    """
    promote_field_to_dimension used to write subsetValues to every promoted field without it ever
    being enforced. Now that subsetValues restricts the choices of a dimension field, it must not
    silently restrict promoted fields.
    """
    Form = apps.get_model("forms", "Form")

    for form in Form.objects.all():
        changed = False
        for field_list in (form.fields, form.cached_enriched_fields):
            for field in field_list:
                if "subsetValues" in field:
                    del field["subsetValues"]
                    changed = True
        if changed:
            form.save(update_fields=["fields", "cached_enriched_fields"])


class Migration(migrations.Migration):
    dependencies = [  # noqa: RUF012
        ("forms", "0059_survey_followup_purpose_and_parent"),
    ]

    operations = [  # noqa: RUF012
        migrations.RunPython(
            code=clear_subset_values,
            reverse_code=migrations.RunPython.noop,
            elidable=True,
        ),
    ]
