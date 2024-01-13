import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0001_initial"),
        ("labour", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Perk",
            fields=[
                ("id", models.AutoField(verbose_name="ID", serialize=False, auto_created=True, primary_key=True)),
                (
                    "slug",
                    models.CharField(
                        help_text='Tekninen nimi eli "slug" n\xe4kyy URL-osoitteissa. Sallittuja merkkej\xe4 ovat pienet kirjaimet, numerot ja v\xe4liviiva. Teknist\xe4 nime\xe4 ei voi muuttaa luomisen j\xe4lkeen.',
                        max_length=63,
                        verbose_name="Tekninen nimi",
                        validators=[
                            django.core.validators.RegexValidator(
                                regex="[a-z0-9-]+",
                                message="Tekninen nimi saa sis\xe4lt\xe4\xe4 vain pieni\xe4 kirjaimia, numeroita sek\xe4 v\xe4liviivoja.",
                            )
                        ],
                    ),
                ),
                ("name", models.CharField(max_length=63)),
                ("event", models.ForeignKey(on_delete=models.CASCADE, to="core.Event")),
            ],
            options={
                "verbose_name": "etu",
                "verbose_name_plural": "edut",
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name="PersonnelClass",
            fields=[
                ("id", models.AutoField(verbose_name="ID", serialize=False, auto_created=True, primary_key=True)),
                ("app_label", models.CharField(default="", max_length=63, blank=True)),
                ("name", models.CharField(max_length=63)),
                (
                    "slug",
                    models.CharField(
                        help_text='Tekninen nimi eli "slug" n\xe4kyy URL-osoitteissa. Sallittuja merkkej\xe4 ovat pienet kirjaimet, numerot ja v\xe4liviiva. Teknist\xe4 nime\xe4 ei voi muuttaa luomisen j\xe4lkeen.',
                        max_length=63,
                        verbose_name="Tekninen nimi",
                        validators=[
                            django.core.validators.RegexValidator(
                                regex="[a-z0-9-]+",
                                message="Tekninen nimi saa sis\xe4lt\xe4\xe4 vain pieni\xe4 kirjaimia, numeroita sek\xe4 v\xe4liviivoja.",
                            )
                        ],
                    ),
                ),
                ("priority", models.IntegerField(default=0)),
                ("event", models.ForeignKey(on_delete=models.CASCADE, to="core.Event")),
                ("perks", models.ManyToManyField(to="labour.Perk", blank=True)),
            ],
            options={
                "ordering": ("event", "priority"),
                "verbose_name": "henkil\xf6st\xf6luokka",
                "verbose_name_plural": "henkil\xf6st\xf6luokat",
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name="personnelclass",
            unique_together={("event", "slug")},
        ),
        migrations.AlterIndexTogether(
            name="personnelclass",
            index_together={("event", "app_label")},
        ),
        migrations.AlterUniqueTogether(
            name="perk",
            unique_together={("event", "slug")},
        ),
        migrations.AddField(
            model_name="signup",
            name="personnel_classes",
            field=models.ManyToManyField(to="labour.PersonnelClass", blank=True),
            preserve_default=True,
        ),
    ]
