# Generated by Django 2.2.9 on 2020-01-27 18:59

from django.db import migrations, models
import django.db.models.deletion
import labour.models.signup_extras


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("core", "0033_auto_20191111_1851"),
        ("enrollment", "0008_auto_20190409_2051"),
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
                        default=False, verbose_name="Haluan todistuksen työskentelystäni Popcult Helsingissä"
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
                        related_name="popcult2020_signup_extras",
                        to="core.Event",
                    ),
                ),
                (
                    "person",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="popcult2020_signup_extra",
                        to="core.Person",
                    ),
                ),
                (
                    "special_diet",
                    models.ManyToManyField(
                        blank=True,
                        related_name="popcult2020_signupextra",
                        to="enrollment.SpecialDiet",
                        verbose_name="Erikoisruokavalio",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=(labour.models.signup_extras.SignupExtraMixin, models.Model),
        ),
    ]
