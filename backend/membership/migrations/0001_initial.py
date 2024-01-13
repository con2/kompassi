from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0005_auto_20151008_2225"),
        ("auth", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Membership",
            fields=[
                ("id", models.AutoField(verbose_name="ID", serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
                "verbose_name": "J\xe4senyys",
                "verbose_name_plural": "J\xe4senyydet",
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name="MembershipOrganizationMeta",
            fields=[
                (
                    "organization",
                    models.OneToOneField(
                        on_delete=models.CASCADE,
                        primary_key=True,
                        serialize=False,
                        to="core.Organization",
                        verbose_name="Organisaatio",
                    ),
                ),
                (
                    "admin_group",
                    models.ForeignKey(
                        on_delete=models.CASCADE, verbose_name="Yll\xe4pit\xe4j\xe4ryhm\xe4", to="auth.Group"
                    ),
                ),
            ],
            options={
                "verbose_name": "J\xe4senrekisterien asetukset",
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name="membership",
            name="organization",
            field=models.ForeignKey(on_delete=models.CASCADE, verbose_name="Organisaatio", to="core.Organization"),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name="membership",
            name="person",
            field=models.ForeignKey(on_delete=models.CASCADE, verbose_name="Henkil\xf6", to="core.Person"),
            preserve_default=True,
        ),
    ]
