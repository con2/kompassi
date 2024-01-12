from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("labour", "0013_signup_time_confirmation_requested"),
    ]

    operations = [
        migrations.AlterField(
            model_name="signup",
            name="job_categories_accepted",
            field=models.ManyToManyField(
                help_text="Teht\xe4v\xe4alueet, joilla hyv\xe4ksytty vapaaehtoisty\xf6ntekij\xe4 tulee ty\xf6skentelem\xe4\xe4n. T\xe4m\xe4n perusteella henkil\xf6lle mm. l\xe4hetet\xe4\xe4n oman teht\xe4v\xe4alueensa ty\xf6voimaohjeet. Harmaalla merkityt teht\xe4v\xe4alueet ovat niit\xe4, joihin hakija ei ole itse hakenut.",
                related_name="accepted_signup_set",
                verbose_name="Hyv\xe4ksytyt teht\xe4v\xe4alueet",
                to="labour.JobCategory",
                blank=True,
            ),
        ),
    ]
