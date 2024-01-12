# Generated by Django 1.9.5 on 2016-07-05 19:40


from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("programme", "0039_programmefeedback"),
    ]

    operations = [
        migrations.AddField(
            model_name="programme",
            name="video_link",
            field=models.CharField(
                blank=True,
                default="",
                help_text="A link to a recording of the programme in an external video service such as YouTube",
                max_length=255,
                verbose_name="Video link",
            ),
        ),
        migrations.AlterField(
            model_name="programmefeedback",
            name="programme",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, related_name="feedback", to="programme.Programme"
            ),
        ),
    ]
