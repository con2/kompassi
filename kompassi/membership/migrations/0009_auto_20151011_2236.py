from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [  # noqa: RUF012
        ("membership", "0008_auto_20151011_2229"),
    ]

    operations = [  # noqa: RUF012
        migrations.AlterModelOptions(
            name="membershipfeepayment",
            options={"verbose_name": "J\xe4senmaksusuoritus", "verbose_name_plural": "J\xe4senmaksusuoritukset"},
        ),
    ]
