from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("yukicon2016", "0002_auto_20151107_1903"),
    ]

    operations = [
        migrations.AlterField(
            model_name="signupextra",
            name="want_certificate",
            field=models.BooleanField(
                default=False, verbose_name="Haluan todistuksen ty\xf6skentelyst\xe4ni Yukiconissa"
            ),
        ),
    ]
