from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("access", "0005_email_aliases"),
    ]

    operations = [
        migrations.AddField(
            model_name="groupemailaliasgrant",
            name="active_until",
            field=models.DateTimeField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name="emailalias",
            name="type",
            field=models.ForeignKey(
                on_delete=models.CASCADE,
                related_name="email_aliases",
                verbose_name="Tyyppi",
                to="access.EmailAliasType",
            ),
            preserve_default=True,
        ),
    ]
