from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ("aicon2016", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="signupextra",
            name="email_alias",
            field=models.CharField(
                default="",
                validators=[
                    django.core.validators.RegexValidator(
                        regex="[a-z0-9-]+",
                        message="Tekninen nimi saa sis\xe4lt\xe4\xe4 vain pieni\xe4 kirjaimia, numeroita sek\xe4 v\xe4liviivoja.",
                    )
                ],
                max_length=32,
                blank=True,
                help_text='Vastaavat saavat k\xe4ytt\xf6\xf6ns\xe4 s\xe4hk\xf6postialiakset, jotka ovat muotoa teht\xe4v\xe4@aicon.fi. Mik\xe4li tied\xe4t jo Aiconin vastaavateht\xe4v\xe4si, sy\xf6t\xe4 se t\xe4h\xe4n mahdollisimman yksinkertaisessa muodossa (esim. pj, ty\xf6voima, ohjelma ym). Osoitteessa isot kirjaimet muutetaan automaattisesti pieniksi, \xe4 a:ksi ja niin edelleen. N\xe4et lopullisen osoitteesi <a href="/profile/aliases" target="_blank">profiilin s\xe4hk\xf6postialiassivulta</a> sitten, kun vastaavailmoittautumisesi on hyv\xe4ksytty. Mik\xe4li osoitteisiin tarvitaan t\xe4m\xe4n j\xe4lkeen muutoksia, Japsu auttaa.',
                verbose_name="S\xe4hk\xf6postialias",
            ),
            preserve_default=True,
        ),
    ]
