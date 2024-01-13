from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0005_auto_20151008_2225"),
    ]

    operations = [
        migrations.AddField(
            model_name="organization",
            name="description",
            field=models.TextField(verbose_name="Kuvaus", blank=True),
            preserve_default=True,
        ),
    ]
