# Generated by Django 4.1.3 on 2022-11-06 17:03

from django.db import migrations, models
import django.db.models.deletion
import labour.models.signup_extras


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("core", "0037_alter_organization_panel_css_class"),
    ]

    operations = [
        migrations.CreateModel(
            name="SpecialDiet",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=63)),
            ],
        ),
        migrations.CreateModel(
            name="SignupExtra",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("is_active", models.BooleanField(default=True)),
                (
                    "shift_type",
                    models.CharField(
                        choices=[
                            ("2h", "2 tunnin vuoroja"),
                            ("4h", "4 tunnin vuoroja"),
                            ("yli4h", "Yli 4 tunnin vuoroja"),
                        ],
                        help_text="Haluatko tehdä yhden pitkän työvuoron vaiko monta lyhyempää vuoroa?",
                        max_length=15,
                        verbose_name="Toivottu työvuoron pituus",
                    ),
                ),
                (
                    "total_work",
                    models.CharField(
                        choices=[("8h", "8 tuntia"), ("yli8h", "Yli 8 tuntia")],
                        help_text="Kuinka paljon haluat tehdä töitä yhteensä tapahtuman aikana? Useimmissa tehtävistä minimi on kahdeksan tuntia, mutta joissain tehtävissä se voi olla myös vähemmän (esim. majoitusvalvonta 6 h).",
                        max_length=15,
                        verbose_name="Toivottu kokonaistyömäärä",
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
                    "prior_experience",
                    models.TextField(
                        blank=True,
                        help_text="Kerro tässä kentässä, jos sinulla on aiempaa kokemusta vastaavista tehtävistä tai muuta sellaista työkokemusta, josta arvioit olevan hyötyä hakemassasi tehtävässä.",
                        verbose_name="Työkokemus",
                    ),
                ),
                (
                    "free_text",
                    models.TextField(
                        blank=True,
                        help_text="Jos haluat sanoa hakemuksesi käsittelijöille jotain sellaista, jolle ei ole omaa kenttää yllä, käytä tätä kenttää.",
                        verbose_name="Vapaa alue",
                    ),
                ),
                (
                    "event",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="%(app_label)s_signup_extras",
                        to="core.event",
                    ),
                ),
                (
                    "person",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="%(app_label)s_signup_extra",
                        to="core.person",
                    ),
                ),
                (
                    "special_diet",
                    models.ManyToManyField(blank=True, to="kuplii2023.specialdiet", verbose_name="Erikoisruokavalio"),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=(labour.models.signup_extras.SignupExtraMixin, models.Model),
        ),
    ]
