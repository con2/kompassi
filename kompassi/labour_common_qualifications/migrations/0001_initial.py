import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("labour", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="JVKortti",
            fields=[
                (
                    "personqualification",
                    models.OneToOneField(
                        on_delete=models.CASCADE,
                        related_name="+",
                        primary_key=True,
                        serialize=False,
                        to="labour.PersonQualification",
                    ),
                ),
                (
                    "card_number",
                    models.CharField(
                        help_text="Muoto: 0000/J0000/00",
                        max_length="13",
                        verbose_name="JV-kortin numero",
                        validators=[
                            django.core.validators.RegexValidator(
                                regex="\\d\\d\\d\\d/J\\d\\d\\d\\d/\\d\\d", message="Tarkista JV-kortin numero"
                            )
                        ],
                    ),
                ),
                ("expiration_date", models.DateField(verbose_name="Viimeinen voimassaolop\xe4iv\xe4")),
            ],
            options={
                "verbose_name": "JV-kortti",
                "verbose_name_plural": "JV-kortit",
            },
            bases=(models.Model,),
        ),
    ]
