import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("labour_common_qualifications", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="jvkortti",
            name="card_number",
            field=models.CharField(
                help_text="Muoto: 0000/J0000/00 tai XX/0000/00",
                max_length="13",
                verbose_name="JV-kortin numero",
                validators=[
                    django.core.validators.RegexValidator(regex=".+/.+/.+", message="Tarkista JV-kortin numero")
                ],
            ),
            preserve_default=True,
        ),
    ]
