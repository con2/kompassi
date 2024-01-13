from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("tickets", "0004_auto_20150125_1601"),
    ]

    operations = [
        migrations.AddField(
            model_name="ticketseventmeta",
            name="print_logo_height_mm",
            field=models.IntegerField(
                default=0,
                help_text="E-lippuun printattavan logon korkeus millimetrein\xe4. Suositellaan noin 20 millimetri\xe4 korkeaa logoa.",
                verbose_name="Logon korkeus (mm)",
            ),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name="ticketseventmeta",
            name="print_logo_path",
            field=models.CharField(
                default="",
                help_text="T\xe4m\xe4 logo printataan e-lippuun.",
                max_length=255,
                verbose_name="Logon polku",
                blank=True,
            ),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name="ticketseventmeta",
            name="print_logo_width_mm",
            field=models.IntegerField(
                default=0,
                help_text="E-lippuun printattavan logon leveys millimetrein\xe4. Suositellaan noin 40 millimetri\xe4 leve\xe4\xe4 logoa.",
                verbose_name="Logon leveys (mm)",
            ),
            preserve_default=True,
        ),
    ]
