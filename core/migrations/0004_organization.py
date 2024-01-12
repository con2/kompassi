import django.core.validators
from django.db import migrations, models

from ..utils import slugify


def populate_organization(apps, schema_editor):
    Organization = apps.get_model("core", "organization")
    Event = apps.get_model("core", "event")

    for event in Event.objects.all():
        event.organization, created = Organization.objects.get_or_create(
            slug=slugify(event.organization_name),
            defaults=dict(
                name=event.organization_name,
                homepage_url=event.organization_url,
            ),
        )
        event.save()


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0003_auto_20150813_1907"),
    ]

    operations = [
        migrations.CreateModel(
            name="Organization",
            fields=[
                ("id", models.AutoField(verbose_name="ID", serialize=False, auto_created=True, primary_key=True)),
                (
                    "slug",
                    models.CharField(
                        help_text='Tekninen nimi eli "slug" n\xe4kyy URL-osoitteissa. Sallittuja merkkej\xe4 ovat pienet kirjaimet, numerot ja v\xe4liviiva. Teknist\xe4 nime\xe4 ei voi muuttaa luomisen j\xe4lkeen.',
                        unique=True,
                        max_length=63,
                        verbose_name="Tekninen nimi",
                        validators=[
                            django.core.validators.RegexValidator(
                                regex="[a-z0-9-]+",
                                message="Tekninen nimi saa sis\xe4lt\xe4\xe4 vain pieni\xe4 kirjaimia, numeroita sek\xe4 v\xe4liviivoja.",
                            )
                        ],
                    ),
                ),
                ("name", models.CharField(max_length=255, verbose_name="Nimi")),
                ("homepage_url", models.CharField(max_length=255, verbose_name="Kotisivu", blank=True)),
            ],
            options={},
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name="event",
            name="organization",
            field=models.ForeignKey(
                on_delete=models.CASCADE,
                verbose_name="J\xe4rjest\xe4j\xe4taho",
                blank=True,
                to="core.Organization",
                null=True,
            ),
            preserve_default=True,
        ),
        migrations.RunPython(populate_organization, elidable=True),
    ]
