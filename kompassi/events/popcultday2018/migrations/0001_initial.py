# Generated by Django 1.10.8 on 2018-01-21 18:04
import django.db.models.deletion
from django.db import migrations, models

import kompassi.labour.models.signup_extras


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("enrollment", "0005_auto_20170928_1334"),
        ("core", "0029_auto_20170827_1818"),
    ]

    operations = [
        migrations.CreateModel(
            name="SignupExtra",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("is_active", models.BooleanField(default=True)),
                (
                    "want_certificate",
                    models.BooleanField(
                        default=False, verbose_name="Haluan todistuksen työskentelystäni Popcult Dayssa"
                    ),
                ),
                (
                    "special_diet_other",
                    models.TextField(
                        blank=True,
                        help_text="Jos noudatat erikoisruokavaliota, jota ei ole yllä olevassa listassa, ilmoita se tässä. Tapahtuman järjestäjä pyrkii ottamaan erikoisruokavaliot huomioon, mutta kaikkia erikoisruokavalioita ei välttämättä pystytä järjestämään.",
                        verbose_name="Muu erikoisruokavalio",
                    ),
                ),
                (
                    "y_u",
                    models.TextField(
                        blank=True,
                        help_text="Miksi juuri sinä sopisit hakemaasi työtehtävään? Voit kertoa itsestäsi vapaamuotoisesti: harrastukset, koulutus, hullu-kissanainen/vähemmän-hullu-koiraihminen yms.",
                        verbose_name="Miksi juuri sinä?",
                    ),
                ),
                (
                    "prior_experience",
                    models.TextField(
                        blank=True,
                        help_text="Kerro aikaisemmasta työkokemuksestasi tapahtuman työvoimana tai muusta kokemuksesta, josta koet olevan hyötyä haetussa/haetuissa työtehtävissä.",
                        verbose_name="Työkokemus",
                    ),
                ),
                (
                    "free_text",
                    models.TextField(
                        blank=True,
                        help_text="Tässä kentässä voit kertoa jotain minkä koet tarpeelliseksi, jota ei ole vielä mainittu.",
                        verbose_name="Lisätietoja",
                    ),
                ),
                (
                    "event",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="popcultday2018_signup_extras",
                        to="core.Event",
                    ),
                ),
                (
                    "person",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="popcultday2018_signup_extra",
                        to="core.Person",
                    ),
                ),
                (
                    "special_diet",
                    models.ManyToManyField(
                        blank=True,
                        related_name="popcultday2018_signupextra",
                        to="enrollment.SpecialDiet",
                        verbose_name="Erikoisruokavalio",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=(kompassi.labour.models.signup_extras.SignupExtraMixin, models.Model),
        ),
    ]
