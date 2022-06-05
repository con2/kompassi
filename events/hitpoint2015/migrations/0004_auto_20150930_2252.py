from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ("hitpoint2015", "0003_auto_20150930_2248"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="signupextra",
            name="lodging_needs",
        ),
        migrations.DeleteModel(
            name="Night",
        ),
        migrations.AddField(
            model_name="signupextra",
            name="need_lodging",
            field=models.BooleanField(
                default=False, verbose_name="Tarvitsen lattiamajoitusta lauantain ja sunnuntain v\xe4liseksi y\xf6ksi"
            ),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name="signupextra",
            name="night_work",
            field=models.CharField(
                help_text="Y\xf6t\xf6it\xe4 voi olla ainoastaan lauantain ja sunnuntain v\xe4lisen\xe4 y\xf6n\xe4.",
                max_length=5,
                verbose_name="Voitko ty\xf6skennell\xe4 y\xf6ll\xe4?",
                choices=[
                    ("miel", "Ty\xf6skentelen mielell\xe4ni y\xf6vuorossa"),
                    ("tarv", "Voin tarvittaessa ty\xf6skennell\xe4 y\xf6vuorossa"),
                    ("ei", "En vaan voi ty\xf6skennell\xe4 y\xf6vuorossa"),
                ],
            ),
            preserve_default=True,
        ),
    ]
