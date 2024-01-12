# Generated by Django 1.9.9 on 2016-10-22 19:45


from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("access", "0013_auto_20160608_0018"),
    ]

    operations = [
        migrations.AddField(
            model_name="emailaliastype",
            name="priority",
            field=models.IntegerField(
                default=0,
                help_text="When determining the e-mail address of a person in relation to a specific event, the e-mail alias type with the smallest priority number wins.",
                verbose_name="priority",
            ),
        ),
    ]
