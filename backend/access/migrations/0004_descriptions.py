from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("access", "0003_slackaccess"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="slackaccess",
            options={"verbose_name": "Slack-kutsuautomaatti", "verbose_name_plural": "Slack-kutsuautomaatit"},
        ),
        migrations.AlterField(
            model_name="slackaccess",
            name="api_token",
            field=models.CharField(default="test", max_length=255, verbose_name="API-koodi"),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name="slackaccess",
            name="team_name",
            field=models.CharField(max_length=255, verbose_name="Slack-yhteis\xf6n nimi"),
            preserve_default=True,
        ),
    ]
