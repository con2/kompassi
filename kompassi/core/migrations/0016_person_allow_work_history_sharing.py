from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0015_organization_name_genitive"),
    ]

    operations = [
        migrations.AddField(
            model_name="person",
            name="allow_work_history_sharing",
            field=models.BooleanField(
                default=False,
                help_text="Mik\xe4li et anna t\xe4h\xe4n lupaa, tapahtuman ty\xf6voimavastaavalle n\xe4ytet\xe4\xe4n ainoastaan ty\xf6skentelysi aikaisemmissa saman organisaation j\xe4rjest\xe4miss\xe4 tapahtumissa.",
                verbose_name="Ty\xf6skentelyhistoriani saa n\xe4ytt\xe4\xe4 kokonaisuudessaan niille tapahtumille, joihin haen vapaaehtoisty\xf6h\xf6n <i>(vapaaehtoinen)</i>",
            ),
            preserve_default=True,
        ),
    ]
