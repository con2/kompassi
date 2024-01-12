# Generated by Django 1.9.9 on 2016-10-20 18:43


from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("intra", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="teammember",
            name="person",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, related_name="team_memberships", to="core.Person"
            ),
        ),
    ]
