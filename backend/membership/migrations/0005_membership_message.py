from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("membership", "0004_auto_20151010_1632"),
    ]

    operations = [
        migrations.AddField(
            model_name="membership",
            name="message",
            field=models.TextField(verbose_name="Viesti hakemuksen k\xe4sittelij\xe4lle", blank=True),
            preserve_default=True,
        ),
    ]
