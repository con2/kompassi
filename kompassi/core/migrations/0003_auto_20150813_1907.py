from django.db import migrations, models

import kompassi.core.models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0002_auto_20150126_1611"),
    ]

    operations = [
        migrations.AlterField(
            model_name="person",
            name="birth_date",
            field=models.DateField(
                blank=True,
                help_text="Syntym\xe4aika muodossa 24.2.1994",
                null=True,
                verbose_name="Syntym\xe4aika",
                validators=[kompassi.core.models.birth_date_validator],
            ),
            preserve_default=True,
        ),
    ]
