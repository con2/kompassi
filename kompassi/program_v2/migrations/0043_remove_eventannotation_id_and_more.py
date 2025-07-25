# Generated by Django 5.2.3 on 2025-07-19 16:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("program_v2", "0042_annotation_eventannotation_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="eventannotation",
            name="id",
        ),
        migrations.RemoveField(
            model_name="programv2eventmeta",
            name="annotations",
        ),
        migrations.AddField(
            model_name="eventannotation",
            name="pk",
            field=models.CompositePrimaryKey(
                "meta", "annotation", blank=True, editable=False, primary_key=True, serialize=False
            ),
        ),
        migrations.AlterField(
            model_name="eventannotation",
            name="annotation",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="all_event_annotations",
                to="program_v2.annotation",
            ),
        ),
        migrations.AlterField(
            model_name="eventannotation",
            name="meta",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="all_event_annotations",
                to="program_v2.programv2eventmeta",
            ),
        ),
    ]
