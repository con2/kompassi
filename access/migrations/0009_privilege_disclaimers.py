from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ("access", "0008_smtp"),
    ]

    operations = [
        migrations.AddField(
            model_name="privilege",
            name="disclaimers",
            field=models.TextField(blank=True),
            preserve_default=True,
        ),
    ]
