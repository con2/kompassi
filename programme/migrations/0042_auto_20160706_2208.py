# Generated by Django 1.9.5 on 2016-07-06 19:08


from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("programme", "0041_programme_rerun"),
    ]

    operations = [
        migrations.AlterField(
            model_name="programme",
            name="rerun",
            field=models.CharField(
                choices=[
                    ("already", "Yes, the programme has previously been presented in another convention"),
                    ("will", "Yes, the programme will be presented in a convention that takes place before this one"),
                    ("might", "The programme might be presented in a convention that takes place before this one"),
                    (
                        "original",
                        "The programme is original to this convention and I promise not to present it elsewhere before",
                    ),
                ],
                default="original",
                help_text="Have you presented this same programme at another event before the event you are offering it to now, or do you intend to present it in another event before this one? If you are unsure about the re-run policy of this event, please consult the programme managers.",
                max_length=8,
                verbose_name="Is your programme original to this event, or a re-run from another event?",
            ),
        ),
    ]
