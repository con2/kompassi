from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0009_auto_20151010_1632"),
    ]

    operations = [
        migrations.AddField(
            model_name="organization",
            name="public",
            field=models.BooleanField(
                default=False,
                help_text="Julkisilla yhdistyksill\xe4 on yhdistyssivu ja ne n\xe4ytet\xe4\xe4n etusivulla.",
                verbose_name="Julkinen",
            ),
            preserve_default=True,
        ),
    ]
