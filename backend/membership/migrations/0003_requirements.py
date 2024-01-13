from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("membership", "0002_membershiporganizationmeta_receiving_applications"),
    ]

    operations = [
        migrations.AddField(
            model_name="membershiporganizationmeta",
            name="membership_fee",
            field=models.TextField(
                default="",
                help_text="Mink\xe4 suuruinen on liittymis- ja j\xe4senmaksu ja miten se maksetaan?",
                verbose_name="J\xe4senmaksu",
            ),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name="membershiporganizationmeta",
            name="membership_requirements",
            field=models.TextField(
                default="",
                help_text="Esim. copy-paste s\xe4\xe4nn\xf6ist\xe4.",
                verbose_name="Kuka voi hakea j\xe4senyytt\xe4?",
            ),
            preserve_default=True,
        ),
    ]
