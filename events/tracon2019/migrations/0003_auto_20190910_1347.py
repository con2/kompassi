# Generated by Django 2.1.12 on 2019-09-10 10:47

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("tracon2019", "0002_auto_20190909_2157"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="signupextra",
            name="afterparty_coaches_changed",
        ),
        migrations.RemoveField(
            model_name="signupextra",
            name="outward_coach_departure_time",
        ),
        migrations.RemoveField(
            model_name="signupextra",
            name="return_coach_departure_time",
        ),
        migrations.RemoveField(
            model_name="signupextra",
            name="willing_to_bartend",
        ),
        migrations.AddField(
            model_name="signupextra",
            name="afterparty_help",
            field=models.TextField(
                blank=True,
                default="",
                help_text="Oletko valmis auttamaan kaadon järjestelyissä, esim. logistiikassa, roudauksessa tai juomien kaatamisessa? Kirjoita tähän, millaisia hommia olisit valmis tekemään ja kuinka paljon (karkea tuntimäärä illan aikana).",
                verbose_name="Työskentely kaatajaisissa",
            ),
        ),
        migrations.AlterField(
            model_name="signupextra",
            name="afterparty_participation",
            field=models.BooleanField(
                default=False,
                help_text='Ruksaa tämä ruutu, mikäli haluat osallistua kaatajaisiin. Mikäli mielesi muuttuu tai sinulle tulee este, peru ilmoittautumisesi poistamalla rasti tästä ruudusta. Muistathan tällöin vapauttaa myös mahdollisen <a href="/profile/reservations" target="_blank">paikkasi kaatobussissa</a>.',
                verbose_name="Osallistun kaatajaisiin",
            ),
        ),
    ]
