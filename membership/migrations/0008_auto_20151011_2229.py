from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0014_auto_20151011_2016"),
        ("membership", "0007_auto_20151011_2109"),
    ]

    operations = [
        migrations.CreateModel(
            name="MembershipFeePayment",
            fields=[
                ("id", models.AutoField(verbose_name="ID", serialize=False, auto_created=True, primary_key=True)),
                ("payment_date", models.DateField(auto_now_add=True)),
                (
                    "member",
                    models.ForeignKey(
                        on_delete=models.CASCADE, related_name="membership_fee_payments", to="membership.Membership"
                    ),
                ),
            ],
            options={},
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name="Term",
            fields=[
                ("id", models.AutoField(verbose_name="ID", serialize=False, auto_created=True, primary_key=True)),
                ("title", models.CharField(help_text="Yleens\xe4 vuosiluku", max_length=63, verbose_name="Otsikko")),
                (
                    "start_date",
                    models.DateField(
                        help_text="Yleens\xe4 vuoden ensimm\xe4inen p\xe4iv\xe4", verbose_name="Alkamisp\xe4iv\xe4"
                    ),
                ),
                (
                    "end_date",
                    models.DateField(
                        help_text="Yleens\xe4 vuoden viimeinen p\xe4iv\xe4", verbose_name="P\xe4\xe4ttymisp\xe4iv\xe4"
                    ),
                ),
                (
                    "entrance_fee_cents",
                    models.PositiveIntegerField(
                        default=0,
                        help_text="Arvo 0 (nolla sentti\xe4) tarkoittaa, ett\xe4 yhdistyksell\xe4 ei ole t\xe4ll\xe4 kaudella liittymismaksua. Arvon puuttuminen tarkoittaa, ett\xe4 liittymismaksu ei ole tiedossa.",
                        null=True,
                        verbose_name="Liittymismaksu (snt)",
                        blank=True,
                    ),
                ),
                (
                    "membership_fee_cents",
                    models.PositiveIntegerField(
                        default=0,
                        help_text="Arvo 0 (nolla sentti\xe4) tarkoittaa, ett\xe4 yhdistyksell\xe4 ei ole t\xe4ll\xe4 kaudella j\xe4senmaksua. Arvon puuttuminen tarkoittaa, ett\xe4 liittymismaksu ei ole tiedossa.",
                        null=True,
                        verbose_name="J\xe4senmaksu (snt)",
                        blank=True,
                    ),
                ),
                (
                    "organization",
                    models.ForeignKey(
                        on_delete=models.CASCADE, related_name="terms", verbose_name="Yhdistys", to="core.Organization"
                    ),
                ),
            ],
            options={
                "verbose_name": "Toimikausi",
                "verbose_name_plural": "Toimikaudet",
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name="membershipfeepayment",
            name="term",
            field=models.ForeignKey(
                on_delete=models.CASCADE, related_name="membership_fee_payments", to="membership.Term"
            ),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name="membership",
            name="organization",
            field=models.ForeignKey(
                on_delete=models.CASCADE, related_name="members", verbose_name="Yhdistys", to="core.Organization"
            ),
            preserve_default=True,
        ),
    ]
