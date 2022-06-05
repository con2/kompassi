from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ("animecon2015", "0003_auto_20150303_2332"),
    ]

    operations = [
        migrations.AddField(
            model_name="signupextra",
            name="personal_identification_number",
            field=models.CharField(
                verbose_name="Henkil\xf6tunnus",
                max_length=12,
                blank=True,
                default="",
                help_text="HUOM! T\xe4yt\xe4 t\xe4m\xe4 kentt\xe4 vain, jos haet <strong>kortittomaksi j\xe4rjestyksenvalvojaksi</strong>.",
            ),
            preserve_default=True,
        ),
    ]
