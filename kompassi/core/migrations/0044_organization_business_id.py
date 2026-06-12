from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0043_emailverificationtoken_language_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="organization",
            name="business_id",
            field=models.CharField(
                blank=True,
                default="",
                max_length=16,
                verbose_name="Y-tunnus",
                help_text="Finnish business ID (Y-tunnus), eg. 1234567-8.",
            ),
        ),
    ]
