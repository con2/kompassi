import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


def populate_original_created_fields(apps, schema_editor):
    Response = apps.get_model("forms", "Response")

    for response in Response.objects.all():
        current_response = response.superseded_by or response
        old_versions = Response.objects.filter(superseded_by=current_response).order_by("-revision_created_at")
        original = old_versions.first() or response

        response.original_created_at = original.revision_created_at
        response.original_created_by = original.revision_created_by
        response.save(update_fields=["original_created_at", "original_created_by"])


class Migration(migrations.Migration):
    dependencies = [
        ("forms", "0044_response_superseded_by_and_more"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameField(
            model_name="response",
            old_name="created_at",
            new_name="revision_created_at",
        ),
        migrations.RenameField(
            model_name="response",
            old_name="created_by",
            new_name="revision_created_by",
        ),
        migrations.RemoveField(
            model_name="response",
            name="updated_at",
        ),
        migrations.AddField(
            model_name="response",
            name="original_created_at",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="response",
            name="original_created_by",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="response",
            name="revision_created_by",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.RunPython(
            code=populate_original_created_fields,
            reverse_code=migrations.RunPython.noop,
            elidable=True,
        ),
    ]
