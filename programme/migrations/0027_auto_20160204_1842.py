# Generated by Django 1.9.1 on 2016-02-04 16:42


from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("programme", "0026_auto_20160202_2238"),
    ]

    operations = [
        migrations.AddField(
            model_name="programme",
            name="computer",
            field=models.CharField(
                choices=[
                    ("con", "Laptop provided by the event"),
                    ("pc", "Own laptop \u2013 PC"),
                    ("mac", "Own laptop \u2013\xa0Mac"),
                    ("none", "No computer required"),
                ],
                default="con",
                help_text="The use of your own computer is only possible if agreed in advance.",
                max_length=4,
                verbose_name="What kind of a computer do you wish to use?",
            ),
        ),
        migrations.AddField(
            model_name="programme",
            name="encumbered_content",
            field=models.CharField(
                choices=[
                    ("yes", "My programme contains copyright-encumbered audio or video"),
                    ("no", "My programme does not contain copyright-encumbered audio or video"),
                    ("notsure", "I'm not sure whether my programme contains copyright-encumbered content or not"),
                ],
                default="no",
                help_text="Encumbered content cannot be displayed on our YouTube channel. Encumbered content will be edited out of video recordings.",
                max_length=7,
                verbose_name="Encumbered content",
            ),
        ),
        migrations.AddField(
            model_name="programme",
            name="number_of_microphones",
            field=models.IntegerField(
                choices=[
                    (0, "0"),
                    (1, "1"),
                    (2, "2"),
                    (3, "3"),
                    (4, "4"),
                    (5, "5"),
                    (
                        99,
                        'More than five \u2013\xa0Please elaborate on your needs in the "Other tech requirements" field.',
                    ),
                ],
                default=1,
                verbose_name="How many microphones do you require?",
            ),
        ),
        migrations.AddField(
            model_name="programme",
            name="photography",
            field=models.CharField(
                choices=[
                    ("please", "Please photograph my programme"),
                    ("okay", "It's OK to photograph my programme"),
                    ("nope", "Please do not photograph my programme"),
                ],
                default="okay",
                help_text="Our official photographers will try to cover all programmes whose hosts request their programmes to be photographed.",
                max_length=6,
                verbose_name="Photography of your prorgmme",
            ),
        ),
        migrations.AddField(
            model_name="programme",
            name="use_audio",
            field=models.CharField(
                choices=[("yes", "Yes"), ("no", "No"), ("notsure", "Not sure")],
                default="no",
                max_length=7,
                verbose_name="Will you play audio in your programme?",
            ),
        ),
        migrations.AddField(
            model_name="programme",
            name="use_video",
            field=models.CharField(
                choices=[("yes", "Yes"), ("no", "No"), ("notsure", "Not sure")],
                default="no",
                max_length=7,
                verbose_name="Will you play video in your programme?",
            ),
        ),
        migrations.AlterField(
            model_name="programme",
            name="tech_requirements",
            field=models.TextField(
                blank=True,
                help_text="Do you have tech requirements that are not covered by the previous questions?",
                verbose_name="Tech requirements",
            ),
        ),
        migrations.AlterIndexTogether(
            name="programme",
            index_together={("category", "state")},
        ),
    ]
