from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("core", "0003_auto_20150813_1907"),
    ]

    operations = [
        migrations.CreateModel(
            name="ConfirmationCode",
            fields=[
                ("id", models.AutoField(verbose_name="ID", serialize=False, auto_created=True, primary_key=True)),
                ("code", models.CharField(unique=True, max_length=63)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("used_at", models.DateTimeField(null=True, blank=True)),
                (
                    "state",
                    models.CharField(
                        default="valid",
                        max_length=8,
                        choices=[("valid", "Kelvollinen"), ("used", "K\xe4ytetty"), ("revoked", "Mit\xe4t\xf6ity")],
                    ),
                ),
                ("desuprofile_id", models.IntegerField()),
                ("person", models.ForeignKey(on_delete=models.CASCADE, to="core.Person")),
            ],
            options={
                "abstract": False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name="Connection",
            fields=[
                ("id", models.IntegerField(serialize=False, verbose_name="Desuprofiilin numero", primary_key=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=models.CASCADE,
                        verbose_name="K\xe4ytt\xe4j\xe4",
                        to=settings.AUTH_USER_MODEL,
                        unique=True,
                    ),
                ),
            ],
            options={},
            bases=(models.Model,),
        ),
        migrations.AlterIndexTogether(
            name="confirmationcode",
            index_together={("person", "state")},
        ),
    ]
