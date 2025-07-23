from django.db import migrations, models

import kompassi.mailings.models


class Migration(migrations.Migration):
    dependencies = [
        ("auth", "0001_initial"),
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Message",
            fields=[
                ("id", models.AutoField(verbose_name="ID", serialize=False, auto_created=True, primary_key=True)),
                ("subject_template", models.CharField(max_length=255, verbose_name="Otsikko")),
                (
                    "body_template",
                    models.TextField(
                        help_text="Teksti {{ signup.formatted_job_categories_accepted }} korvataan listalla hyv\xe4ksytyn v\xe4nk\xe4rin teht\xe4v\xe4alueista ja teksti {{ signup.formatted_shifts }} korvataan v\xe4nk\xe4rin vuoroilla.",
                        verbose_name="Viestin teksti",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("sent_at", models.DateTimeField(null=True, blank=True)),
                ("expired_at", models.DateTimeField(null=True, blank=True)),
            ],
            options={
                "verbose_name": "viesti",
                "verbose_name_plural": "viestit",
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name="PersonMessage",
            fields=[
                ("id", models.AutoField(verbose_name="ID", serialize=False, auto_created=True, primary_key=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={},
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name="PersonMessageBody",
            fields=[
                ("id", models.AutoField(verbose_name="ID", serialize=False, auto_created=True, primary_key=True)),
                ("digest", models.CharField(max_length=63, db_index=True)),
                ("text", models.TextField()),
            ],
            options={},
            bases=(models.Model, kompassi.mailings.models.DedupMixin),
        ),
        migrations.CreateModel(
            name="PersonMessageSubject",
            fields=[
                ("id", models.AutoField(verbose_name="ID", serialize=False, auto_created=True, primary_key=True)),
                ("digest", models.CharField(max_length=63, db_index=True)),
                ("text", models.CharField(max_length=255)),
            ],
            options={},
            bases=(models.Model, kompassi.mailings.models.DedupMixin),
        ),
        migrations.CreateModel(
            name="RecipientGroup",
            fields=[
                ("id", models.AutoField(verbose_name="ID", serialize=False, auto_created=True, primary_key=True)),
                (
                    "app_label",
                    models.CharField(max_length=63, verbose_name="Sovellus", choices=[("labour", "Ty\xc3\xb6voima")]),
                ),
                ("verbose_name", models.CharField(max_length=63, verbose_name="Nimi")),
                ("event", models.ForeignKey(on_delete=models.CASCADE, verbose_name="Tapahtuma", to="core.Event")),
                (
                    "group",
                    models.ForeignKey(
                        on_delete=models.CASCADE, verbose_name="K\xe4ytt\xe4j\xe4ryhm\xe4", to="auth.Group"
                    ),
                ),
            ],
            options={
                "verbose_name": "vastaanottajaryhm\xe4",
                "verbose_name_plural": "vastaanottajaryhm\xe4t",
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name="personmessage",
            name="body",
            field=models.ForeignKey(on_delete=models.CASCADE, to="mailings.PersonMessageBody"),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name="personmessage",
            name="message",
            field=models.ForeignKey(on_delete=models.CASCADE, to="mailings.Message"),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name="personmessage",
            name="person",
            field=models.ForeignKey(on_delete=models.CASCADE, to="core.Person"),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name="personmessage",
            name="subject",
            field=models.ForeignKey(on_delete=models.CASCADE, to="mailings.PersonMessageSubject"),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name="message",
            name="recipient",
            field=models.ForeignKey(
                on_delete=models.CASCADE, verbose_name="Vastaanottajaryhm\xe4", to="mailings.RecipientGroup"
            ),
            preserve_default=True,
        ),
    ]
