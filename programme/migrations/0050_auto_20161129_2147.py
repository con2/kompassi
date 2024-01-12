# Generated by Django 1.9.9 on 2016-11-29 19:47


import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0023_auto_20160704_2155"),
        ("hitpoint2017", "0003_timeslot"),
        ("programme", "0049_programmerole_is_active"),
    ]

    operations = [
        migrations.CreateModel(
            name="AlternativeProgrammeForm",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "slug",
                    models.CharField(
                        help_text='Tekninen nimi eli "slug" n\xe4kyy URL-osoitteissa. Sallittuja merkkej\xe4 ovat pienet kirjaimet, numerot ja v\xe4liviiva. Teknist\xe4 nime\xe4 ei voi muuttaa luomisen j\xe4lkeen.',
                        max_length=255,
                        validators=[
                            django.core.validators.RegexValidator(
                                message="Tekninen nimi saa sis\xe4lt\xe4\xe4 vain pieni\xe4 kirjaimia, numeroita sek\xe4 v\xe4liviivoja.",
                                regex="[a-z0-9-]+",
                            )
                        ],
                        verbose_name="Tekninen nimi",
                    ),
                ),
                (
                    "title",
                    models.CharField(
                        help_text="This title is visible to the programme host.", max_length=63, verbose_name="title"
                    ),
                ),
                (
                    "description",
                    models.TextField(
                        blank=True,
                        default="",
                        help_text="Visible to the hosts that register their programmes using this form.",
                        null=True,
                        verbose_name="description",
                    ),
                ),
                (
                    "short_description",
                    models.TextField(
                        blank=True,
                        default="",
                        help_text="Visible on the page that offers different kinds of forms.",
                        null=True,
                        verbose_name="short description",
                    ),
                ),
                (
                    "programme_form_code",
                    models.CharField(
                        help_text="A reference to the form class that implements the form. Example: hitpoint2017.forms:RolePlayingGameForm",
                        max_length=63,
                    ),
                ),
                ("active_from", models.DateTimeField(blank=True, null=True, verbose_name="Active from")),
                ("active_until", models.DateTimeField(blank=True, null=True, verbose_name="Active until")),
                (
                    "num_extra_invites",
                    models.PositiveIntegerField(
                        default=5,
                        help_text="To support programmes with multiple hosts, the host offering the programme may be enabled to invite more hosts to their programme by entering their e-mail addresses. This field controls if this is available and at most how many e-mail addresses may be entered.",
                        verbose_name="Number of extra invites",
                    ),
                ),
                ("order", models.IntegerField(default=0)),
                (
                    "event",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="core.Event", verbose_name="event"
                    ),
                ),
            ],
            options={
                "ordering": ("event", "order", "title"),
                "verbose_name": "alternative programme form",
                "verbose_name_plural": "alternative programme forms",
            },
        ),
        migrations.CreateModel(
            name="ColdOffersProgrammeEventMetaProxy",
            fields=[],
            options={
                "proxy": True,
            },
            bases=("programme.programmeeventmeta",),
        ),
        migrations.AddField(
            model_name="programme",
            name="approximate_length",
            field=models.IntegerField(
                blank=True,
                default=240,
                help_text="Please give your best guess on how long you expect your game to take.",
                null=True,
                verbose_name="approximate length (minutes)",
            ),
        ),
        migrations.AddField(
            model_name="programme",
            name="hitpoint2017_preferred_time_slots",
            field=models.ManyToManyField(
                help_text="When would you like to run your RPG? The time slots are intentionally vague. If you have more specific needs regarding the time, please explain them in the last open field.",
                to="hitpoint2017.TimeSlot",
                verbose_name="preferred time slots",
            ),
        ),
        migrations.AddField(
            model_name="programme",
            name="is_age_restricted",
            field=models.BooleanField(
                default=False,
                help_text="Please tick this box if your game contains themes that require it to be restricted to players of 18 years and older.",
                verbose_name="restricted to people of age 18 and over",
            ),
        ),
        migrations.AddField(
            model_name="programme",
            name="is_beginner_friendly",
            field=models.BooleanField(
                default=False,
                help_text="Please tick this box if your game can be enjoyed even without any prior role-playing experience.",
                verbose_name="beginner friendly",
            ),
        ),
        migrations.AddField(
            model_name="programme",
            name="is_children_friendly",
            field=models.BooleanField(
                default=False,
                help_text="Please tick this box if your game is suitable for younger players. Please give more details, if necessary, in the last open field.",
                verbose_name="children-friendly",
            ),
        ),
        migrations.AddField(
            model_name="programme",
            name="is_english_ok",
            field=models.BooleanField(
                default=False,
                help_text="Please tick this box if you are able, prepared and willing to host your programme in English if necessary.",
                verbose_name="English OK",
            ),
        ),
        migrations.AddField(
            model_name="programme",
            name="is_intended_for_experienced_participants",
            field=models.BooleanField(default=False, verbose_name="experienced participants preferred"),
        ),
        migrations.AddField(
            model_name="programme",
            name="max_players",
            field=models.PositiveIntegerField(
                default=4,
                help_text="What is the maximum number of players that can take part in a single run of the game?",
                validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(99)],
                verbose_name="maximum number of players",
            ),
        ),
        migrations.AddField(
            model_name="programme",
            name="min_players",
            field=models.PositiveIntegerField(
                default=1,
                help_text="How many players must there at least be for the game to take place?",
                validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(99)],
                verbose_name="minimum number of players",
            ),
        ),
        migrations.AddField(
            model_name="programme",
            name="other_author",
            field=models.CharField(
                blank=True,
                default="",
                help_text="If the scenario has been written by someone else than the GM, we require that the author be disclosed.",
                max_length=1023,
                verbose_name="Author (if other than the GM)",
            ),
        ),
        migrations.AddField(
            model_name="programme",
            name="physical_play",
            field=models.CharField(
                choices=[("lots", "Lots of it"), ("some", "Some"), ("none", "Not at all")],
                default="some",
                help_text="In this context, physical play can mean, for example, using your whole body, acting the actions of your character or moving around in the allocated space.",
                max_length=4,
                verbose_name="Amount of physical play",
            ),
        ),
        migrations.AddField(
            model_name="programme",
            name="rpg_system",
            field=models.CharField(
                blank=True,
                default="",
                help_text="Which rule system is your RPG using?",
                max_length=512,
                verbose_name="RPG system",
            ),
        ),
        migrations.AddField(
            model_name="programme",
            name="three_word_description",
            field=models.CharField(
                blank=True,
                default="",
                help_text="Describe your game in three words: for example, genre, theme and attitude.",
                max_length=1023,
                verbose_name="Three-word description",
            ),
        ),
        migrations.AlterField(
            model_name="programme",
            name="description",
            field=models.TextField(
                blank=True,
                default="",
                help_text="This description is published in the web schedule and the programme booklet. The purpose of this description is to give the participant sufficient information to decide whether to take part or not and to market your programme to the participants. We reserve the right to edit the description.",
                verbose_name="Description",
            ),
        ),
        migrations.AddField(
            model_name="programme",
            name="form_used",
            field=models.ForeignKey(
                blank=True,
                help_text="Which form was used to offer this Programme? If null, the default form was used.",
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="programme.AlternativeProgrammeForm",
                verbose_name="form used",
            ),
        ),
        migrations.AlterUniqueTogether(
            name="alternativeprogrammeform",
            unique_together={("event", "slug")},
        ),
    ]
