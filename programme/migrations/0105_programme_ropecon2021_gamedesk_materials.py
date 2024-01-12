# Generated by Django 2.2.17 on 2021-02-24 17:49

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("programme", "0104_auto_20210223_2306"),
    ]

    operations = [
        migrations.AddField(
            model_name="programme",
            name="ropecon2021_gamedesk_materials",
            field=models.TextField(
                blank=True,
                default="",
                help_text="Specify here whether your players are expected to bring their own game tools or other equipment and what that equipment is (e.g. card decks, figure armies)",
                null=True,
                verbose_name="Does your programme require materials from the players?",
            ),
        ),
    ]
