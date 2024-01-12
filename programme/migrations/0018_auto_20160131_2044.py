# Generated by Django 1.9.1 on 2016-01-31 18:44


from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("labour", "0016_auto_20160128_1805"),
        ("programme", "0017_freeformorganizeradminproxy"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="role",
            options={"ordering": ("priority", "title"), "verbose_name": "role", "verbose_name_plural": "roles"},
        ),
        migrations.AddField(
            model_name="role",
            name="personnel_class",
            field=models.ForeignKey(
                blank=True,
                help_text="If the members of this programme role should have a badge, please point this field to their personnel class.",
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="labour.PersonnelClass",
                verbose_name="Personnel class",
            ),
        ),
        migrations.AddField(
            model_name="role",
            name="priority",
            field=models.IntegerField(
                default=0,
                help_text="If a host is involved in multiple Programmes in a single event, to determine their entitlement to a badge and other perks, lowest priority number wins.",
                verbose_name="Priority",
            ),
        ),
    ]
