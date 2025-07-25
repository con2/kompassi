# Generated by Django 4.2.8 on 2023-12-28 15:28

import django.db.models.deletion
from django.db import migrations, models

import kompassi.labour.models.signup_extras


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0039_alter_person_birth_date_alter_person_email_and_more"),
        ("hitpoint2024", "0003_delete_signupextra"),
    ]

    operations = [
        migrations.CreateModel(
            name="SignupExtra",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("is_active", models.BooleanField(default=True)),
                (
                    "shift_type",
                    models.CharField(
                        choices=[
                            ("yksipitka", "Yksi pitkä vuoro"),
                            ("montalyhytta", "Monta lyhyempää vuoroa"),
                            ("kaikkikay", "Kumpi tahansa käy"),
                        ],
                        help_text="Haluatko tehdä yhden pitkän työvuoron vaiko monta lyhyempää vuoroa?",
                        max_length=15,
                        verbose_name="Toivottu työvuoron pituus",
                    ),
                ),
                (
                    "total_work",
                    models.CharField(
                        choices=[
                            ("6h", "Minimi – 6 tuntia"),
                            ("12h", "10–12 tuntia"),
                            ("yli12h", "Työn Sankari! Yli 12 tuntia!"),
                        ],
                        help_text="Kuinka paljon haluat tehdä töitä yhteensä tapahtuman aikana? Minimi on 6 tuntia.",
                        max_length=15,
                        verbose_name="Toivottu kokonaistyömäärä",
                    ),
                ),
                (
                    "night_work",
                    models.CharField(
                        choices=[
                            ("miel", "Työskentelen mielelläni yövuorossa"),
                            ("tarv", "Voin tarvittaessa työskennellä yövuorossa"),
                            ("ei", "En vaan voi työskennellä yövuorossa"),
                        ],
                        help_text="Yötöitä voi olla ainoastaan lauantain ja sunnuntain välisenä yönä.",
                        max_length=5,
                        verbose_name="Voitko työskennellä yöllä?",
                    ),
                ),
                (
                    "construction",
                    models.BooleanField(
                        default=False,
                        help_text="Huomaathan, että perjantain ja lauantain väliselle yölle ei ole tarjolla majoitusta.",
                        verbose_name="Voin työskennellä jo perjantaina",
                    ),
                ),
                (
                    "want_certificate",
                    models.BooleanField(default=False, verbose_name="Haluan todistuksen työskentelystäni Hitpointissa"),
                ),
                (
                    "certificate_delivery_address",
                    models.TextField(
                        blank=True,
                        help_text="Jos haluat työtodistuksen, täytä tähän kenttään postiosoite (katuosoite, postinumero ja postitoimipaikka) johon haluat todistuksen toimitettavan.",
                        verbose_name="Työtodistuksen toimitusosoite",
                    ),
                ),
                (
                    "shirt_size",
                    models.CharField(
                        choices=[
                            ("NO_SHIRT", "Ei paitaa"),
                            ("BEANIE", "Pipo"),
                            ("XS", "Paita – XS Unisex"),
                            ("S", "Paita – S Unisex"),
                            ("M", "Paita – M Unisex"),
                            ("L", "Paita – L Unisex"),
                            ("XL", "Paita – XL Unisex"),
                            ("XXL", "Paita – XXL Unisex"),
                            ("3XL", "Paita – 3XL Unisex"),
                            ("4XL", "Paita – 4XL Unisex"),
                            ("5XL", "Paita – 5XL Unisex"),
                            ("LF_S", "Paita – S Ladyfit"),
                            ("LF_M", "Paita – M Ladyfit"),
                            ("LF_L", "Paita – L Ladyfit"),
                            ("LF_XL", "Paita – XL Ladyfit"),
                        ],
                        default="NO_SHIRT",
                        help_text='Ajoissa ilmoittautuneet vänkärit saavat maksuttoman työvoimapaidan tai pipon. Valitse tässä, haluatko pipon vai paidan, ja paidan tapauksessa myös paidan koko. Kokotaulukot: <a href="https://dc-collection.fi/product/TU03T" target="_blank" rel="noopener noreferrer">unisex-paita</a>, <a href="https://dc-collection.fi/product/TW04T" target="_blank" rel="noopener noreferrer">ladyfit-paita</a>',
                        max_length=8,
                        verbose_name="Swägivalinta",
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
                    "need_lodging",
                    models.BooleanField(
                        default=False, verbose_name="Tarvitsen lattiamajoitusta lauantain ja sunnuntain väliseksi yöksi"
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
                    "shift_wishes",
                    models.TextField(
                        blank=True,
                        help_text="Jos tiedät nyt jo, ettet pääse paikalle johonkin tiettyyn aikaan tai haluat osallistua johonkin tiettyyn ohjelmanumeroon, mainitse siitä tässä.",
                        verbose_name="Alustavat työvuorotoiveet",
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
                    "afterparty_participation",
                    models.BooleanField(
                        default=False,
                        help_text="Ruksaa tämä ruutu, mikäli haluat osallistua kaatajaisiin. Mikäli mielesi muuttuu tai sinulle tulee este, peru ilmoittautumisesi poistamalla rasti tästä ruudusta. ",
                        verbose_name="Osallistun kaatajaisiin",
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
                    models.ManyToManyField(blank=True, to="hitpoint2024.specialdiet", verbose_name="Erikoisruokavalio"),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=(kompassi.labour.models.signup_extras.SignupExtraMixin, models.Model),
        ),
    ]
