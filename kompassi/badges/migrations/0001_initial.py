import django.core.validators
from django.db import migrations, models

import kompassi.badges.models
import kompassi.core.csv_export


class Migration(migrations.Migration):
    dependencies = [
        ("auth", "0001_initial"),
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Badge",
            fields=[
                ("id", models.AutoField(verbose_name="ID", serialize=False, auto_created=True, primary_key=True)),
                ("printed_separately_at", models.DateTimeField(null=True, blank=True)),
                ("revoked_at", models.DateTimeField(null=True, blank=True)),
                (
                    "job_title",
                    models.CharField(default="", max_length=63, verbose_name="Teht\xe4v\xe4nimike", blank=True),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Luotu")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="P\xe4ivitetty")),
            ],
            options={},
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name="BadgesEventMeta",
            fields=[
                (
                    "event",
                    models.OneToOneField(
                        on_delete=models.CASCADE,
                        related_name="badgeseventmeta",
                        primary_key=True,
                        serialize=False,
                        to="core.Event",
                    ),
                ),
                (
                    "badge_factory_code",
                    models.CharField(
                        default="badges.utils:default_badge_factory",
                        help_text="Funktio, joka selvitt\xe4\xe4, mink\xe4 tyyppinen badge henkil\xf6lle pit\xe4isi luoda. Oletusarvo toimii, jos tapahtumalla on tasan yksi badgepohja. Ks. esimerkkitoteutus tracon9/badges.py:badge_factory.",
                        max_length="255",
                        verbose_name="Badgetehdas",
                    ),
                ),
                ("admin_group", models.ForeignKey(on_delete=models.CASCADE, to="auth.Group")),
            ],
            options={
                "abstract": False,
            },
            bases=(models.Model, kompassi.badges.models.CountBadgesMixin),
        ),
        migrations.CreateModel(
            name="Batch",
            fields=[
                ("id", models.AutoField(verbose_name="ID", serialize=False, auto_created=True, primary_key=True)),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Luotu")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="P\xe4ivitetty")),
                ("printed_at", models.DateTimeField(null=True, blank=True)),
                ("event", models.ForeignKey(on_delete=models.CASCADE, related_name="badge_batch_set", to="core.Event")),
            ],
            options={},
            bases=(models.Model, kompassi.core.csv_export.CsvExportMixin),
        ),
        migrations.CreateModel(
            name="Template",
            fields=[
                ("id", models.AutoField(verbose_name="ID", serialize=False, auto_created=True, primary_key=True)),
                (
                    "slug",
                    models.CharField(
                        help_text='Tekninen nimi eli "slug" n\xe4kyy URL-osoitteissa. Sallittuja merkkej\xe4 ovat pienet kirjaimet, numerot ja v\xe4liviiva. Teknist\xe4 nime\xe4 ei voi muuttaa luomisen j\xe4lkeen.',
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
                ("name", models.CharField(max_length=63)),
                ("event", models.ForeignKey(on_delete=models.CASCADE, to="core.Event")),
            ],
            options={
                "verbose_name": "Badgepohja",
                "verbose_name_plural": "Badgepohjat",
            },
            bases=(models.Model, kompassi.badges.models.CountBadgesMixin),
        ),
        migrations.AlterUniqueTogether(
            name="template",
            unique_together={("event", "slug")},
        ),
        migrations.AddField(
            model_name="batch",
            name="template",
            field=models.ForeignKey(on_delete=models.CASCADE, blank=True, to="badges.Template", null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name="badge",
            name="batch",
            field=models.ForeignKey(on_delete=models.CASCADE, blank=True, to="badges.Batch", null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name="badge",
            name="person",
            field=models.ForeignKey(on_delete=models.CASCADE, blank=True, to="core.Person", null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name="badge",
            name="template",
            field=models.ForeignKey(on_delete=models.CASCADE, verbose_name="Badgetyyppi", to="badges.Template"),
            preserve_default=True,
        ),
    ]
