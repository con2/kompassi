import django.db.models.deletion
from django.db import migrations, models

import kompassi.emprinten.models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="FileVersion",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("data", models.FileField(upload_to=kompassi.emprinten.models.make_filename)),
                ("version", models.PositiveIntegerField(default=1)),
                ("current", models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name="Project",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=255)),
                ("slug", models.SlugField(unique=True)),
                (
                    "split_output",
                    models.BooleanField(
                        help_text="If set, produce a zip archive containing one or more PDFs instead of a single PDF."
                    ),
                ),
                (
                    "name_pattern",
                    models.CharField(
                        blank=True,
                        help_text="File name template pattern without file extension. Gets row dictionary as context unless rendering multiple rows and Split output is not set.",
                        max_length=255,
                    ),
                ),
                (
                    "title_pattern",
                    models.CharField(
                        help_text="PDF title template pattern. Gets row dictionary as context unless rendering multiple rows and Split output is not set.",
                        max_length=255,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ProjectFile",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("file_name", models.CharField(max_length=255, unique=True)),
                (
                    "type",
                    models.CharField(
                        choices=[("main", "Main"), ("html", "Html"), ("css", "Css"), ("csv", "Csv"), ("img", "Image")],
                        max_length=4,
                    ),
                ),
                ("hidden", models.BooleanField(default=False)),
                ("editable", models.BooleanField(default=False)),
                ("transient", models.BooleanField(default=False)),
                ("project", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="emprinten.project")),
            ],
        ),
        migrations.AddField(
            model_name="fileversion",
            name="file",
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="emprinten.projectfile"),
        ),
        migrations.AddConstraint(
            model_name="fileversion",
            constraint=models.UniqueConstraint(
                condition=models.Q(("current", True)), fields=("file",), name="unique_current_file"
            ),
        ),
        migrations.AlterUniqueTogether(
            name="fileversion",
            unique_together={("file", "version")},
        ),
    ]
