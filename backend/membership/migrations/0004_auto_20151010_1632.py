from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("membership", "0003_requirements"),
    ]

    operations = [
        migrations.AddField(
            model_name="membership",
            name="state",
            field=models.CharField(
                default="in_effect",
                max_length=10,
                choices=[
                    ("approval", "Odottaa hyv\xe4ksynt\xe4\xe4"),
                    ("in_effect", "Voimassa"),
                    ("discharged", "Erotettu"),
                ],
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="membershiporganizationmeta",
            name="membership_fee",
            field=models.TextField(
                default="",
                help_text="Mink\xe4 suuruinen on liittymis- ja j\xe4senmaksu ja miten se maksetaan?",
                verbose_name="J\xe4senmaksu",
                blank=True,
            ),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name="membershiporganizationmeta",
            name="membership_requirements",
            field=models.TextField(
                default="",
                help_text="Esim. copy-paste s\xe4\xe4nn\xf6ist\xe4.",
                verbose_name="Kuka voi hakea j\xe4senyytt\xe4?",
                blank=True,
            ),
            preserve_default=True,
        ),
    ]
