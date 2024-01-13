from datetime import timedelta

from django.db import migrations, models


def populate_end_times(apps, schema_editor):
    Programme = apps.get_model("programme", "programme")
    for programme in Programme.objects.all():
        if programme.start_time and programme.length:
            programme.end_time = programme.start_time + timedelta(minutes=programme.length)
            programme.save()


class Migration(migrations.Migration):
    dependencies = [
        ("programme", "0004_auto_20151024_1644"),
    ]

    operations = [
        migrations.AddField(
            model_name="programme",
            name="end_time",
            field=models.DateTimeField(null=True, verbose_name="P\xe4\xe4ttymisaika", blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name="tag",
            name="title",
            field=models.CharField(max_length=63),
            preserve_default=True,
        ),
        migrations.RunPython(populate_end_times, elidable=True),
    ]
