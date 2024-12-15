from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("program_v2", "0031_scheduleitemdimensionvalue"),
    ]

    operations = [
        migrations.AlterField(
            model_name="program",
            name="title",
            field=models.TextField(blank=True, default=""),
        ),
        migrations.RenameField(
            model_name="program",
            old_name="description",
            new_name="description_fi",
        ),
        migrations.RenameField(
            model_name="program",
            old_name="title",
            new_name="title_fi",
        ),
        migrations.AddField(
            model_name="program",
            name="description_en",
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name="program",
            name="description_sv",
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name="program",
            name="title_en",
            field=models.TextField(blank=True, default=""),
        ),
        migrations.AddField(
            model_name="program",
            name="title_sv",
            field=models.TextField(blank=True, default=""),
        ),
        migrations.AddField(
            model_name="scheduleitem",
            name="annotations",
            field=models.JSONField(blank=True, default=dict, help_text="Own annotations of this schedule item only."),
        ),
        migrations.AddField(
            model_name="scheduleitem",
            name="cached_annotations",
            field=models.JSONField(
                blank=True,
                default=dict,
                help_text="Combined annotations of this schedule item and its parent program item.",
            ),
        ),
    ]
