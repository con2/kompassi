from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("tickets", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="ticketseventmeta",
            name="front_page_text",
            field=models.TextField(
                default="",
                help_text="T\xe4m\xe4 teksti n\xe4ytet\xe4\xe4n lippukaupan ensimm\xe4isell\xe4 vaiheella.",
                verbose_name="Etusivun teksti",
                blank=True,
            ),
            preserve_default=True,
        ),
    ]
