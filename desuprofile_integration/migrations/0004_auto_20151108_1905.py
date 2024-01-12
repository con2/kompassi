from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("desuprofile_integration", "0003_auto_20151016_2135"),
    ]

    operations = [
        migrations.AlterField(
            model_name="connection",
            name="user",
            field=models.OneToOneField(
                on_delete=models.CASCADE, verbose_name="K\xe4ytt\xe4j\xe4", to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
