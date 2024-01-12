from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("auth", "0001_initial"),
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Batch",
            fields=[
                ("id", models.AutoField(verbose_name="ID", serialize=False, auto_created=True, primary_key=True)),
                ("create_time", models.DateTimeField(auto_now=True)),
                ("delivery_time", models.DateTimeField(null=True, blank=True)),
            ],
            options={
                "verbose_name": "toimituser\xe4",
                "verbose_name_plural": "toimituser\xe4t",
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name="Customer",
            fields=[
                ("id", models.AutoField(verbose_name="ID", serialize=False, auto_created=True, primary_key=True)),
                ("first_name", models.CharField(max_length=100, verbose_name="Etunimi")),
                ("last_name", models.CharField(max_length=100, verbose_name="Sukunimi")),
                ("address", models.CharField(max_length=200, verbose_name="Katuosoite")),
                ("zip_code", models.CharField(max_length=5, verbose_name="Postinumero")),
                ("city", models.CharField(max_length=30, verbose_name="Postitoimipaikka")),
                (
                    "email",
                    models.EmailField(
                        help_text="Tarkista s\xe4hk\xf6postiosoite huolellisesti. Tilausvahvistus sek\xe4 mahdolliset s\xe4hk\xf6iset liput l\xe4hetet\xe4\xe4n t\xe4h\xe4n s\xe4hk\xf6postiosoitteeseen.",
                        max_length=75,
                        verbose_name="S\xe4hk\xf6postiosoite",
                    ),
                ),
                (
                    "allow_marketing_email",
                    models.BooleanField(
                        default=True,
                        verbose_name="Minulle saa l\xe4hett\xe4\xe4 Traconiin liittyvi\xe4 tiedotteita s\xe4hk\xf6postitse",
                    ),
                ),
                ("phone_number", models.CharField(max_length=30, null=True, verbose_name="Puhelinnumero", blank=True)),
            ],
            options={
                "verbose_name": "asiakas",
                "verbose_name_plural": "asiakkaat",
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name="LimitGroup",
            fields=[
                ("id", models.AutoField(verbose_name="ID", serialize=False, auto_created=True, primary_key=True)),
                ("description", models.CharField(max_length=255, verbose_name="Kuvaus")),
                ("limit", models.IntegerField(verbose_name="Enimm\xe4ism\xe4\xe4r\xe4")),
            ],
            options={
                "verbose_name": "loppuunmyyntiryhm\xe4",
                "verbose_name_plural": "loppuunmyyntiryhm\xe4t",
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name="Order",
            fields=[
                ("id", models.AutoField(verbose_name="ID", serialize=False, auto_created=True, primary_key=True)),
                ("start_time", models.DateTimeField(auto_now_add=True)),
                ("confirm_time", models.DateTimeField(null=True, verbose_name="Tilausaika", blank=True)),
                (
                    "ip_address",
                    models.CharField(max_length=15, null=True, verbose_name="Tilaajan IP-osoite", blank=True),
                ),
                ("payment_date", models.DateField(null=True, verbose_name="Maksup\xe4iv\xe4", blank=True)),
                ("cancellation_time", models.DateTimeField(null=True, verbose_name="Peruutusaika", blank=True)),
                ("reference_number", models.CharField(max_length=31, verbose_name="Viitenumero", blank=True)),
                (
                    "batch",
                    models.ForeignKey(
                        on_delete=models.CASCADE,
                        verbose_name="Toimituser\xe4",
                        blank=True,
                        to="tickets.Batch",
                        null=True,
                    ),
                ),
                (
                    "customer",
                    models.OneToOneField(on_delete=models.CASCADE, null=True, blank=True, to="tickets.Customer"),
                ),
            ],
            options={
                "verbose_name": "tilaus",
                "verbose_name_plural": "tilaukset",
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name="OrderProduct",
            fields=[
                ("id", models.AutoField(verbose_name="ID", serialize=False, auto_created=True, primary_key=True)),
                ("count", models.IntegerField(default=0)),
                (
                    "order",
                    models.ForeignKey(on_delete=models.CASCADE, related_name="order_product_set", to="tickets.Order"),
                ),
            ],
            options={
                "verbose_name": "tilausrivi",
                "verbose_name_plural": "tilausrivit",
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name="Product",
            fields=[
                ("id", models.AutoField(verbose_name="ID", serialize=False, auto_created=True, primary_key=True)),
                ("name", models.CharField(max_length=100)),
                ("internal_description", models.CharField(max_length=255, null=True, blank=True)),
                ("description", models.TextField()),
                ("mail_description", models.TextField(null=True, blank=True)),
                ("price_cents", models.IntegerField()),
                ("requires_shipping", models.BooleanField(default=True)),
                ("electronic_ticket", models.BooleanField(default=False)),
                ("available", models.BooleanField(default=True)),
                ("notify_email", models.CharField(max_length=100, null=True, blank=True)),
                ("ordering", models.IntegerField(default=0)),
            ],
            options={
                "verbose_name": "tuote",
                "verbose_name_plural": "tuotteet",
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name="TicketsEventMeta",
            fields=[
                (
                    "event",
                    models.OneToOneField(
                        on_delete=models.CASCADE,
                        related_name="ticketseventmeta",
                        primary_key=True,
                        serialize=False,
                        to="core.Event",
                    ),
                ),
                (
                    "shipping_and_handling_cents",
                    models.IntegerField(default=0, verbose_name="Toimituskulut (senttej\xe4)"),
                ),
                ("due_days", models.IntegerField(default=14, verbose_name="Maksuaika (p\xe4ivi\xe4)")),
                (
                    "ticket_sales_starts",
                    models.DateTimeField(null=True, verbose_name="Lipunmyynnin alkuaika", blank=True),
                ),
                (
                    "ticket_sales_ends",
                    models.DateTimeField(null=True, verbose_name="Lipunmyynnin p\xe4\xe4ttymisaika", blank=True),
                ),
                (
                    "reference_number_template",
                    models.CharField(
                        default="{:04d}",
                        help_text="Paikkamerkin {} kohdalle sijoitetaan tilauksen numero. Nollilla t\xe4ytt\xe4minen esim. {:04d} (4 merkin leveydelt\xe4).",
                        max_length=31,
                        verbose_name="Viitenumeron formaatti",
                    ),
                ),
                (
                    "contact_email",
                    models.CharField(
                        help_text="Ongelmatilanteissa k\xe4ytt\xe4j\xe4\xe4 kehotetaan ottamaan yhteytt\xe4 t\xe4h\xe4n osoitteeseen. Muoto: Tracon 9 -lipunmyynti &lt;liput@tracon.fi&gt;",
                        max_length=255,
                        verbose_name="Asiakaspalvelun s\xe4hk\xf6postiosoite selitteineen",
                        blank=True,
                    ),
                ),
                (
                    "plain_contact_email",
                    models.CharField(
                        help_text="Ongelmatilanteissa k\xe4ytt\xe4j\xe4\xe4 kehotetaan ottamaan yhteytt\xe4 t\xe4h\xe4n osoitteeseen. Muoto: liput@tracon.fi",
                        max_length=255,
                        verbose_name="Asiakaspalvelun s\xe4hk\xf6postiosoite ilman selitett\xe4",
                        blank=True,
                    ),
                ),
                (
                    "ticket_spam_email",
                    models.CharField(
                        help_text="Kaikki j\xe4rjestelm\xe4n l\xe4hett\xe4m\xe4t s\xe4hk\xf6postiviestit l\xe4hetet\xe4\xe4n my\xf6s t\xe4h\xe4n osoitteeseen.",
                        max_length=255,
                        verbose_name="Tarkkailus\xe4hk\xf6posti",
                        blank=True,
                    ),
                ),
                (
                    "reservation_seconds",
                    models.IntegerField(
                        default=1800,
                        help_text="K\xe4ytt\xe4j\xe4ll\xe4 on t\xe4m\xe4n verran aikaa siirty\xe4 maksamaan ja maksaa tilauksensa tai tilaus perutaan.",
                        verbose_name="Varausaika (sekuntia)",
                    ),
                ),
                (
                    "ticket_free_text",
                    models.TextField(
                        help_text="T\xe4m\xe4 teksti tulostetaan E-lippuun.", verbose_name="E-lipun teksti", blank=True
                    ),
                ),
                ("admin_group", models.ForeignKey(on_delete=models.CASCADE, to="auth.Group")),
            ],
            options={
                "verbose_name": "tapahtuman lipunmyyntiasetukset",
                "verbose_name_plural": "tapahtuman lipunmyyntiasetukset",
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name="product",
            name="event",
            field=models.ForeignKey(on_delete=models.CASCADE, to="core.Event"),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name="product",
            name="limit_groups",
            field=models.ManyToManyField(to="tickets.LimitGroup", blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name="orderproduct",
            name="product",
            field=models.ForeignKey(on_delete=models.CASCADE, related_name="order_product_set", to="tickets.Product"),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name="order",
            name="event",
            field=models.ForeignKey(on_delete=models.CASCADE, to="core.Event"),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name="limitgroup",
            name="event",
            field=models.ForeignKey(on_delete=models.CASCADE, verbose_name="Tapahtuma", to="core.Event"),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name="batch",
            name="event",
            field=models.ForeignKey(on_delete=models.CASCADE, to="core.Event"),
            preserve_default=True,
        ),
    ]
