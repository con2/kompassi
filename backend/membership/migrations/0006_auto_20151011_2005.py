from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("membership", "0005_membership_message"),
    ]

    operations = [
        migrations.AlterField(
            model_name="membership",
            name="organization",
            field=models.ForeignKey(
                on_delete=models.CASCADE, related_name="members", verbose_name="Organisaatio", to="core.Organization"
            ),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name="membership",
            name="person",
            field=models.ForeignKey(
                on_delete=models.CASCADE, related_name="memberships", verbose_name="Henkil\xf6", to="core.Person"
            ),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name="membershiporganizationmeta",
            name="membership_fee",
            field=models.TextField(
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
                help_text="Esim. copy-paste s\xe4\xe4nn\xf6ist\xe4.",
                verbose_name="Kuka voi hakea j\xe4senyytt\xe4?",
                blank=True,
            ),
            preserve_default=True,
        ),
    ]
