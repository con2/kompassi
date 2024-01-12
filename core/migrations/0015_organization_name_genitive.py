from django.db import migrations, models


def populate_name_genitive(apps, schema_editor):
    Organization = apps.get_model("core", "organization")
    for organization in Organization.objects.all():
        if organization.name and not organization.name_genitive:
            if organization.name.endswith(" ry"):
                organization.name_genitive = organization.name + ":n"
            else:
                organization.name_genitive = organization.name + "n"

        organization.save()


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0014_auto_20151011_2016"),
    ]

    operations = [
        migrations.AddField(
            model_name="organization",
            name="name_genitive",
            field=models.CharField(default="", max_length=255, verbose_name="Nimi genetiiviss\xe4"),
            preserve_default=False,
        ),
        migrations.RunPython(populate_name_genitive, elidable=True),
    ]
