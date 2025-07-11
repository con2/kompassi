from __future__ import annotations

import logging
from datetime import timedelta
from functools import cached_property
from typing import TYPE_CHECKING

from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.db import models
from django.db.models import Q
from django.db.transaction import atomic
from django.utils.timezone import get_default_timezone, now
from django.utils.translation import gettext_lazy as _

from core.csv_export import CsvExportMixin
from core.models import Event
from core.utils import NONUNIQUE_SLUG_FIELD_PARAMS, format_datetime, slugify, url
from core.utils.time_utils import format_interval
from graphql_api.language import get_language_choices

if TYPE_CHECKING:
    from .programme_feedback import ProgrammeFeedback

logger = logging.getLogger("kompassi")


VIDEO_PERMISSION_CHOICES = [
    ("public", _("My programme may be recorded and published")),
    # ('private', _('I forbid publishing my programme, but it may be recorded for archiving purposes')),
    ("forbidden", _("I forbid recording my programme altogether")),
]

STREAM_PERMISSION_CHOICES = [
    ("please", _("Yes, I would like my programme to be streamed live")),
    ("okay", _("Yes, I allow streaming my programme live")),
    ("nope", _("No, I forbid streaming my programme")),
]

START_TIME_LABEL = _("Starting time")

STATE_CHOICES = [
    ("idea", _("Internal programme idea")),
    ("asked", _("Asked from the host")),
    ("offered", _("Offer received")),
    ("accepted", _("Accepted")),
    ("published", _("Published")),
    ("cancelled", _("Cancelled")),
    ("rejected", _("Rejected")),
]

STATE_CSS = dict(
    idea="label-default",
    asked="label-default",
    offered="label-default",
    accepted="label-primary",
    published="label-success",
    cancelled="label-danger",
    rejected="label-danger",
)

COMPUTER_CHOICES = [
    ("con", _("Laptop provided by the event")),
    ("pc", _("Own laptop – PC")),
    ("mac", _("Own laptop – Mac")),
    ("none", _("No computer required")),
]

TRISTATE_CHOICES = [
    ("yes", _("Yes")),
    ("no", _("No")),
    ("notsure", _("Not sure")),
]

TRISTATE_FIELD_PARAMS = dict(
    choices=TRISTATE_CHOICES,
    max_length=max(len(key) for (key, _) in TRISTATE_CHOICES),  # type: ignore
)

ENCUMBERED_CONTENT_CHOICES = [
    ("yes", _("My programme contains copyright-encumbered audio or video")),
    ("no", _("My programme does not contain copyright-encumbered audio or video")),
    ("notsure", _("I'm not sure whether my programme contains copyright-encumbered content or not")),
]

PHOTOGRAPHY_CHOICES = [
    ("please", _("Please photograph my programme")),
    ("okay", _("It's OK to photograph my programme")),
    ("nope", _("Please do not photograph my programme")),
]

RERUN_CHOICES = [
    ("already", _("Yes. The programme has previously been presented in another convention.")),
    ("will", _("Yes. The programme will be presented in a convention that takes place before this one.")),
    ("might", _("Maybe. The programme might be presented in a convention that takes place before this one.")),
    (
        "original",
        _("No. The programme is original to this convention and I promise not to present it elsewhere before."),
    ),
]

PHYSICAL_PLAY_CHOICES = [
    ("lots", _("Lots of it")),
    ("some", _("Some")),
    ("none", _("Not at all")),
]

PROGRAMME_STATES_NEW = ["idea", "asked", "offered"]
PROGRAMME_STATES_LIVE = ["accepted", "published"]
PROGRAMME_STATES_ACTIVE = PROGRAMME_STATES_NEW + PROGRAMME_STATES_LIVE
PROGRAMME_STATES_INACTIVE = ["rejected", "cancelled"]

ROPECON2018_SIGNUP_LIST_CHOICES = [
    ("none", _("No sign-up")),
    ("itse", _("I will collect sign-ups")),
    ("tiski", _("Sign up at the Gaming Desk")),
]

ROPECON2018_KP_LENGTH_CHOICES = [
    ("4h", _("4 hours")),
    ("8h", _("8 hours")),
]

ROPECON2018_KP_DIFFICULTY_CHOICES = [
    ("simple", _("Simple")),
    ("advanced", _("Advanced")),
    ("high", _("Highly Advanced")),
]

ROPECON2018_KP_TABLE_COUNT_CHOICES = [
    ("1", _("1 table")),
    ("2", _("2 tables")),
    ("3", _("3 tables")),
    ("4+", _("4+ tables")),
]

ROPECON2021_GAMEDESK_PHYSICAL_OR_VIRTUAL_CHOICES = [
    ("phys_only", _("I can organize my programme only at a physical con")),
    ("virt_only", _("I can organize my programme only at a virtual con")),
    ("phys_or_virt", _("I can organize my programme both at a physical con and at a virtual con")),
]
ROPECON2021_LARP_PHYSICAL_OR_VIRTUAL_CHOICES = [
    ("physical_only", _("Physical con")),
    ("virtual_only", _("Virtual con")),
    ("physical_or_virtual", _("Both")),
]

ROPECON2023_LANGUAGE_CHOICES = [
    ("finnish", _("Finnish")),
    ("english", _("English")),
    ("language_free", _("Language-free")),
    ("finnish_or_english", _("Finnish or English")),
]

ROPECON2023_SIGNUP_LIST_CHOICES = [
    ("none", _("No sign-up")),
    ("konsti", _("Sign-up via the Konsti app")),
    ("othersign", _("Other sign-up process")),
]

CSV_EXPORT_EXCLUDED_FIELDS = [
    "paikkala_icon",
    "paikkala_program",
]

ROPECON2018_AUDIENCE_SIZE_CHOICES = [
    ("unknown", _("No estimate")),
    ("lt50", _("Less than 50")),
    ("50-100", _("50 – 100")),
    ("100-150", _("100 – 150")),
    ("150-200", _("150 – 200")),
    ("200-250", _("200 – 250")),
    ("gt250", _("Over 250")),
]

SOLMUKOHTA2024_HAVE_YOU_HOSTED_BEFORE_CHOICES = [
    ("", ""),
    ("many", "Yes, many times"),
    ("couple", "Yes, a couple of times"),
    ("few", "Yes, once or twice"),
    ("nope", "No, this is my first time"),
]

ROPECON2024_LANGUAGE_CHOICES = [
    ("finnish", _("Finnish")),
    ("english", _("English")),
    ("language_free", _("Language-free")),
    ("fin_or_eng", _("Finnish or English")),
    ("fin_and_eng", _("Finnish and English")),
    ("other", _("Other")),
]

valid_hex_color = RegexValidator(r"#[\da-fA-F]{3,6}")


class Programme(models.Model, CsvExportMixin):
    """
    Represents a scheduled programme in an event. Usually belongs to a Category and has a start and
    end time. Also usually happens in a Room.

    Note that this is a "dense sparse model" meaning the model covers multiple types of Programme
    some of which have fields that are not used by the others. The fields used are specified by the
    Form used. The default form fits lectures etc. and other types of programme are covered using
    AlternativeProgrammeForms.
    """

    id: int
    pk: int
    feedback: models.Manager[ProgrammeFeedback]

    category = models.ForeignKey(
        "programme.Category",
        on_delete=models.CASCADE,
        verbose_name=_("category"),
        help_text=_("Choose the category that fits your programme the best. We reserve the right to change this."),
    )
    form_used = models.ForeignKey(
        "programme.AlternativeProgrammeForm",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name=_("form used"),
        help_text=_("Which form was used to offer this Programme? If null, the default form was used."),
    )

    slug = models.CharField(**NONUNIQUE_SLUG_FIELD_PARAMS)  # type: ignore

    title = models.CharField(
        max_length=1023,
        verbose_name=_("Title"),
        help_text=_("Make up a concise title for your programme. We reserve the right to edit the title."),
    )

    description = models.TextField(
        blank=True,
        default="",
        verbose_name=_("Description"),
        help_text=_(
            "This description is published in the web schedule and the programme booklet. The purpose of this "
            "description is to give the participant sufficient information to decide whether to take part or "
            "not and to market your programme to the participants. We reserve the right to edit the "
            "description."
        ),
    )
    long_description = models.TextField(
        blank=True,
        default="",
        verbose_name="Tarkempi kuvaus",
        help_text=(
            "Kuvaile ohjelmaasi tarkemmin ohjelmavastaavalle. Minkälaista rakennetta olet ohjelmallesi "
            "suunnitellut? Millaisia asioita tulisit käsittelemään? Kerro myös onko ohjelmasi suunnattu "
            "aloittevammille vai kokeneemmille harrastajille."
        ),
    )
    three_word_description = models.CharField(
        max_length=1023,
        blank=True,
        default="",
        verbose_name=_("Three-word description"),
        help_text=_("Describe your game in three words: for example, genre, theme and attitude."),
    )
    hosts_from_host = models.CharField(
        max_length=1023,
        blank=True,
        default="",
        verbose_name=_("Programme host names"),
        help_text=_(
            "Please provide the names as they should be presented in the programme guide. "
            "Please indicate their role in the programme, if there are multiple roles (moderator, panelist, etc.). "
            "Please also include yourself in the list.",
        ),
    )

    use_audio = models.CharField(
        default="no",
        verbose_name=_("Audio playback"),
        help_text=_("Will you play audio in your programme?"),
        **TRISTATE_FIELD_PARAMS,  # type: ignore
    )

    use_video = models.CharField(
        default="no",
        verbose_name=_("Video playback"),
        help_text=_("Will you play video in your programme?"),
        **TRISTATE_FIELD_PARAMS,  # type: ignore
    )

    number_of_microphones = models.IntegerField(
        default=1,
        verbose_name=_("Microphones"),
        help_text=_("How many microphones do you require?"),
        choices=[
            (0, "0"),
            (1, "1"),
            (2, "2"),
            (3, "3"),
            (4, "4"),
            (5, "5"),
            (
                99,
                _('More than five – Please elaborate on your needs in the "Other tech requirements" field.'),
            ),
        ],
    )

    computer = models.CharField(
        default="con",
        choices=COMPUTER_CHOICES,
        max_length=max(len(key) for (key, label) in COMPUTER_CHOICES),
        verbose_name=_("Computer use"),
        help_text=_(
            "What kind of a computer do you wish to use? The use of your own computer is only possible if "
            "agreed in advance."
        ),
    )

    tech_requirements = models.TextField(
        blank=True,
        verbose_name=_("Other tech requirements"),
        help_text=_("Do you have tech requirements that are not covered by the previous questions?"),
    )

    room_requirements = models.TextField(
        blank=True,
        verbose_name=_("Room requirements"),
        help_text=_(
            "How large an audience do you expect for your programme? What kind of a room do you wish for your "
            "programme?"
        ),
    )

    requested_time_slot = models.TextField(
        blank=True,
        verbose_name=_("Requested time slot"),
        help_text=_(
            "At what time would you like to hold your programme? Are there other programme that you do not "
            "wish to co-incide with?"
        ),
    )

    video_permission = models.CharField(
        max_length=15,
        choices=VIDEO_PERMISSION_CHOICES,
        blank=True,
        verbose_name=_("Recording permission"),
        help_text=_("May your programme be recorded and published in the Internet?"),
    )

    stream_permission = models.CharField(
        max_length=max(len(key) for (key, text) in STREAM_PERMISSION_CHOICES),
        choices=STREAM_PERMISSION_CHOICES,
        blank=True,
        verbose_name=_("Streaming permission"),
        help_text=_(
            "May your programme be streamed live on YouTube? Streamed programmes will also be available afterwards on our channel."
        ),
    )

    encumbered_content = models.CharField(
        blank=True,
        max_length=max(len(key) for (key, label) in ENCUMBERED_CONTENT_CHOICES),
        choices=ENCUMBERED_CONTENT_CHOICES,
        verbose_name=_("Encumbered content"),
        help_text=_(
            "Encumbered content cannot be displayed on our YouTube channel. Encumbered content will be edited "
            "out of video recordings."
        ),
    )

    photography = models.CharField(
        max_length=max(len(key) for (key, label) in PHOTOGRAPHY_CHOICES),
        choices=PHOTOGRAPHY_CHOICES,
        blank=True,
        verbose_name=_("Photography of your programme"),
        help_text=_(
            "Our official photographers will try to cover all programmes whose hosts request their programmes "
            "to be photographed."
        ),
    )

    rerun = models.CharField(
        blank=True,
        max_length=max(len(key) for (key, label) in RERUN_CHOICES),
        choices=RERUN_CHOICES,
        verbose_name=_("Is this a re-run?"),
        help_text=_(
            "Have you presented this same programme at another event before the event you are offering "
            "it to now, or do you intend to present it in another event before this one? If you are unsure "
            "about the re-run policy of this event, please consult the programme managers."
        ),
    )

    rerun_extra = models.TextField(
        blank=True,
        default="",
        verbose_name="Kuvaile uusintaohjelmaa tarkemmin",
        help_text="Jos ohjelmasi on uusinta, kerro tarkemmin missä ja milloin olet sen aikaisemmin pitänyt. Aiotko tehdä muutoksia ohjelmaasi tätä esitystä varten? Millaisia?",
    )

    notes_from_host = models.TextField(
        blank=True,
        verbose_name=_("Anything else?"),
        help_text=_(
            "If there is anything else you wish to say to the programme manager that is not covered by the "
            "above questions, please enter it here."
        ),
    )

    state = models.CharField(
        max_length=15,
        choices=STATE_CHOICES,
        default="accepted",
        verbose_name=_("State"),
        help_text=_(
            'The programmes in the state "Published" will be visible to the general public, if the schedule '
            "has already been published."
        ),
    )

    frozen = models.BooleanField(
        default=False,
        verbose_name=_("Frozen"),
        help_text=_(
            "When a programme is frozen, its details can no longer be edited by the programme host. The "
            "programme manager may continue to edit these, however."
        ),
    )

    start_time = models.DateTimeField(blank=True, null=True, verbose_name=START_TIME_LABEL)

    # denormalized
    end_time = models.DateTimeField(blank=True, null=True, verbose_name=_("Ending time"))

    length = models.IntegerField(
        blank=True,
        null=True,
        verbose_name=_("Length (minutes)"),
        help_text=_(
            "In order to be displayed in the schedule, the programme must have a start time and a length and "
            "must be assigned into a room."
        ),
    )
    length_from_host = models.CharField(
        max_length=127,
        blank=True,
        null=True,
        verbose_name=_("Length of the programme"),
        help_text=(
            "Huomaathan, että emme voi taata juuri toivomasi pituista ohjelmapaikkaa. Ohjelmavastaava vahvistaa "
            "ohjelmasi pituuden."
        ),
    )
    language = models.CharField(
        max_length=2,
        default="fi",
        choices=get_language_choices(),
        verbose_name=_("Language"),
        help_text=_("What is the primary language of your programme?"),
    )
    is_in_english = models.BooleanField(default=False)
    is_inaccessible = models.BooleanField(
        default=False,
        verbose_name=_("Accessibility hazard"),
        help_text=_(
            "If your program contains loud noises, flashing lights or other elements that can limit accessibility, please tick the checkbox. More details can be provided in the last text field if necessary."
        ),
    )

    # Originally hitpoint2017 rpg form fields
    rpg_system = models.CharField(
        max_length=512,
        blank=True,
        default="",
        verbose_name=_("RPG system"),
        help_text=_("Which rule system is your RPG using?"),
    )
    approximate_length = models.IntegerField(
        blank=True,
        null=True,
        default=240,
        verbose_name=_("approximate length (minutes)"),
        help_text=_("Please give your best guess on how long you expect one run of your game to take."),
    )
    max_runs = models.PositiveSmallIntegerField(
        blank=True,
        null=True,
        default=1,
        verbose_name=_("Maximum number of runs"),
        help_text=_("How many times are you prepared to run this game?"),
    )
    physical_play = models.CharField(
        max_length=max(len(key) for (key, text) in PHYSICAL_PLAY_CHOICES),
        default="some",
        choices=PHYSICAL_PLAY_CHOICES,
        verbose_name=_("Amount of physical play"),
        help_text=_(
            "In this context, physical play can mean, for example, using your whole body, acting the actions "
            "of your character or moving around in the allocated space."
        ),
    )
    is_english_ok = models.BooleanField(
        verbose_name=_("English OK"),
        help_text=_(
            "Please tick this box if you are able, prepared and willing to host your programme in English if necessary."
        ),
        default=False,
    )
    is_children_friendly = models.BooleanField(
        verbose_name=_("children-friendly"),
        help_text=_(
            "Please tick this box if your game is suitable for younger players. Please give more details, if "
            "necessary, in the last open field."
        ),
        default=False,
    )
    is_family_program = models.BooleanField(default=False)
    is_age_restricted = models.BooleanField(
        verbose_name=_("restricted to people of age 18 and over"),
        help_text=_(
            "Please tick this box if your game contains themes that require it to be restricted to players of "
            "18 years and older."
        ),
        default=False,
    )
    is_beginner_friendly = models.BooleanField(
        verbose_name=_("beginner friendly"),
        help_text=_("Please tick this box if your game can be enjoyed even without any prior role-playing experience."),
        default=False,
    )
    is_intended_for_experienced_participants = models.BooleanField(
        verbose_name=_("experienced participants preferred"),
        default=False,
    )
    is_available_for_panel = models.BooleanField(
        default=False,
        verbose_name=_("Panel discussions"),
        help_text=_("I can participate in a panel discussion on my field of expertise during the convention."),
    )
    field_of_expertise = models.CharField(
        max_length=1023,
        blank=True,
        default="",
        verbose_name=_("My field of expertise"),
    )
    min_players = models.PositiveIntegerField(
        verbose_name=_("minimum number of players"),
        help_text=_("How many players must there at least be for the game to take place?"),
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(99)],
        null=True,
        blank=True,
    )
    max_players = models.PositiveIntegerField(
        verbose_name=_("maximum number of players"),
        help_text=_("What is the maximum number of players that can take part in a single run of the game?"),
        validators=[MinValueValidator(1), MaxValueValidator(99)],
        null=True,
        blank=True,
    )
    hitpoint2017_preferred_time_slots = models.ManyToManyField(
        "hitpoint2017.TimeSlot",
        verbose_name=_("preferred time slots"),
        help_text=_(
            "When would you like to run your RPG? The time slots are intentionally vague. If you have more "
            "specific needs regarding the time, please explain them in the last open field."
        ),
    )

    hitpoint2020_preferred_time_slots = models.ManyToManyField(
        "hitpoint2020.TimeSlot",
        verbose_name=_("preferred time slots"),
        help_text=_(
            "When would you like to run your RPG? The time slots are intentionally vague. If you have more "
            "specific needs regarding the time, please explain them in the last open field."
        ),
    )

    tracon2023_preferred_time_slots = models.ManyToManyField(
        "tracon2023.TimeSlot",
        verbose_name=_("preferred time slots"),
        help_text=_(
            "When would you like to hold your programme? The time slots are intentionally vague. If you have more "
            "specific needs regarding the time, please explain them in the last open field."
        ),
    )
    tracon2023_accessibility_warnings = models.ManyToManyField(
        "tracon2023.AccessibilityWarning",
        verbose_name=_("Accessibility warnings"),
        blank=True,
    )
    tracon2023_content_warnings = models.TextField(
        default="",
        blank=True,
        verbose_name=_("Content warnings"),
        help_text=_(
            "We will print content warnings in the programme schedule in order to give our visitors the requisite information to make educated choices about programme. If your programme contains bright lights, loud noises, smoke or similar effects, please choose them above. Please include any other content warnings in the text field."
        ),
    )

    # XXX BAD, there needs to be a better way if this becomes a recurring pattern
    ropecon2018_preferred_time_slots = models.ManyToManyField(
        "ropecon2018.TimeSlot",
        verbose_name=_("preferred time slots"),
        help_text=_(
            "When would you like to run your RPG? The time slots are intentionally vague. If you have more "
            "specific needs regarding the time, please explain them in the last open field."
        ),
        blank=True,
    )
    ropecon2019_blocked_time_slots = models.ManyToManyField(
        "ropecon2019.TimeSlot",
        verbose_name=_("When are you unable to run your game?"),
        help_text=_(
            "Tell us when you <strong>can not run</strong> your game. You can write more specific requests in the <em>other information</em> "
            "field below (e.g. <em>I'd like to run my game late in the evening</em>), but here we want information about limitations "
            "set by for example work or bus schedules (for example if you need to leave the venue by 11 PM to get to your "
            "accommodation in time)."
        ),
        blank=True,
        related_name="+",
    )
    ropecon2021_blocked_time_slots = models.ManyToManyField(
        "ropecon2021.TimeSlot",
        verbose_name=_("When are you NOT able to run your larp?"),
        help_text=_(
            "Select the times when you are <b>NOT able</b> to run your larp. In other words, leave the times that you would be able to run your larp unselected!<br/>If you have a more specific request in mind regarding your schedule (for example, you would like to run your larp late at night), please let us know in the Comments section below.<br/>In this section, we would like to know more about how work or volunteer shifts, public transport schedules and other factors might be impacting your schedule. For example, if you need to leave the venue by 11pm to be able to catch the last bus to your accommodation."
        ),
        blank=True,
        related_name="+",
    )
    ropecon2019_preferred_time_slots = models.ManyToManyField(
        "ropecon2019.TimeSlot",
        verbose_name=_("time preferences"),
        help_text=_(
            "When would you like to host your game program? Check the times when you would like to host your game program. If you have more specific needs regarding the timing, please let us know in the Comments field below. We do not restrict your desired times, but we reserve the right to make changes. For example, we would rather have tournaments one after another than at the same time."
        ),
        blank=True,
        related_name="+",
    )
    is_revolving_door = models.BooleanField(
        verbose_name=_("Revolving door game"),
        help_text=_(
            "Check this box if new players can join during gameplay and old players may (or must) leave before the game is over. Please mention this in the game description below, and give more details if necessary."
        ),
        default=False,
    )
    ropecon2019_gaming_desk_subtype = models.CharField(
        max_length=4,
        blank=True,
        verbose_name=_("Game program type"),
        help_text=_(
            "What type of game programme are you offering? Tournament – organising your own game tournament or contest. Demonstration – showcasing, demonstrating and running demo games at the Experience Point. Open game – running games with or without specific scenarios by request. Other – Something other than mentioned above"
        ),
        choices=[
            ("tmnt", _("Tournament")),
            ("demo", _("Demonstration")),
            ("open", _("Open game")),
            ("othr", _("Other")),
        ],
    )
    ropecon2020_suitable_for_children_under_7 = models.BooleanField(
        default=False,
        verbose_name=_("Suitable for children under 7"),
        help_text=_(
            "If your game is aimed at children under 7 years of age, please tick this box. You can also tick this box if your game is suitable for children under 7 years, even if it is not specifically designed for them."
        ),
    )
    ropecon2020_suitable_for_children_aged_7_12 = models.BooleanField(
        default=False,
        verbose_name=_("Suitable for children aged 7-12"),
        help_text=_(
            "If your game is aimed at children 7-12 years of age, please tick this box. You can also tick this box if your game is suitable for children aged 7-12 years, even if it is not specifically designed for them."
        ),
    )
    ropecon2020_suitable_for_children_aged_12_plus = models.BooleanField(
        default=False,
        verbose_name=_("Suitable for children aged 12+"),
        help_text=_(
            "If your game is aimed at children over the age of 12, please tick this box. You can also tick this box if your game is suitable for children aged 12 years and older, even if it is not specifically designed for them."
        ),
    )
    ropecon2020_not_suitable_for_children = models.BooleanField(
        default=False,
        verbose_name=_("Not suitable for children"),
        help_text=_("If your game programme is not suitable for children under 15 years of age, please tick this box."),
    )
    ropecon2020_theme_end_of_the_world = models.BooleanField(
        default=False,
        verbose_name=_("Theme: End of the world"),
        help_text=_("If your game is related to the theme of Ropecon 2020 (end of the world), please tick this box."),
    )
    ropecon2020_theme_dinosaurs = models.BooleanField(
        default=False,
        verbose_name=_("Theme: Dinosaurs"),
        help_text=_(
            "If your game is related to the children’s theme of Ropecon 2020 (dinosaurs), please tick this box."
        ),
    )
    ropecon2020_materials_language = models.CharField(
        max_length=1023,
        default="",
        blank=True,
        verbose_name=_("What language is used in the game materials?"),
    )

    ropecon2021_programme_for_children = models.BooleanField(
        default=False,
        verbose_name=_("Programme for children"),
        help_text=_("If your programme is aimed at children and their guardians, please tick this box."),
    )

    ropecon_theme = models.BooleanField(
        default=False,
        verbose_name=_("Theme: Elements"),
        help_text=_("If your programme is related to the theme of Ropecon 2021, please tick this box."),
    )

    ropecon2021_rpg_clarifications = models.TextField(
        verbose_name=_("Any clarifications?"),
        help_text=_(
            "Specify here if you have any clarifications or if you have anything to expand upon regarding the above questions."
        ),
        blank=True,
        null=True,
        default="",
    )

    ropecon2021_accessibility_loud_sounds = models.BooleanField(
        default=False,
        verbose_name=_("Loud sounds"),
    )

    ropecon2021_accessibility_flashing_lights = models.BooleanField(
        default=False,
        verbose_name=_("Flashing or bright lights"),
    )

    ropecon2021_accessibility_strong_smells = models.BooleanField(
        default=False,
        verbose_name=_("Strong smells"),
    )

    ropecon2021_accessibility_irritate_skin = models.BooleanField(
        default=False,
        verbose_name=_("Materials or substances that irritate the skin"),
    )

    ropecon2021_accessibility_physical_contact = models.BooleanField(
        default=False,
        verbose_name=_("Physical contact and/or low chances of personal space"),
    )

    ropecon2021_accessibility_low_lightning = models.BooleanField(
        default=False,
        verbose_name=_("Darkness/low lighting"),
    )

    ropecon2021_accessibility_moving_around = models.BooleanField(
        default=False,
        verbose_name=_("Participation involves a lot of moving around without a chance for sitting down"),
    )

    ropecon2021_accessibility_video = models.BooleanField(
        default=False,
        verbose_name=_("The programme involves watching a video without subtitles for the hearing impaired"),
    )

    ropecon2021_accessibility_recording = models.BooleanField(
        default=False,
        verbose_name=_(
            "Participation requires listening to a recording that does not have a text version for the hearing impaired"
        ),
    )

    ropecon2021_accessibility_text = models.BooleanField(
        default=False,
        verbose_name=_(
            "Participation involves reading long texts independently, and the texts are not available as recordings for those with visual impairment"
        ),
    )

    ropecon2021_accessibility_colourblind = models.BooleanField(
        default=False,
        verbose_name=_("Material used in the programme can cause problems for the colourblind"),
    )

    ropecon2021_accessibility_inaccessibility = models.TextField(
        verbose_name=_("Other inaccessibility"),
        help_text=_(
            "In the open field, define if necessary what features of your programme may possibly limit or enable participation (e.g. if the programme is available in sign language)."
        ),
        blank=True,
        null=True,
        default="",
    )

    ropecon2021_rpg_physical_or_virtual = models.BooleanField(
        default=False,
        verbose_name=_("If Ropecon is held virtually, I can run my game virtually"),
    )

    ropecon2021_gamedesk_materials = models.TextField(
        verbose_name=_("Does your programme require materials from the players?"),
        help_text=_(
            "Specify here whether your players are expected to bring their own game tools or other equipment and what that equipment is (e.g. card decks, figure armies)."
        ),
        blank=True,
        null=True,
        default="",
    )

    ropecon2022_aimed_at_children_under_10 = models.BooleanField(
        default=False,
        verbose_name=_("Aimed at children under 10 years old"),
        help_text=_("Tick this box if your programme is designed for children under the age of 10."),
    )
    ropecon2022_aimed_at_underage_participants = models.BooleanField(
        default=False,
        verbose_name=_("Aimed at underage participants"),
        help_text=_("Tick this box if your programme is designed for underage participants."),
    )
    ropecon2022_aimed_at_adult_participants = models.BooleanField(
        default=False,
        verbose_name=_("Aimed at adult participants"),
        help_text=_("Tick this box if your programme is designed for adult participants."),
    )

    ropecon2022_accessibility_remaining_one_place = models.BooleanField(
        default=False,
        verbose_name=_(
            "Participation involves a lot of remaining in one place without a chance to take breaks and move around"
        ),
    )

    ropecon2022_content_warnings = models.CharField(
        max_length=1023,
        blank=True,
        default="",
        verbose_name=_(
            "Tell us here if your programme contains heavy subjects that may cause discomfort or distress in some participants"
        ),
        help_text=_("Examples: spiders, violence, phobias or other possibly triggering themes"),
    )
    ropecon2023_blocked_time_slots = models.ManyToManyField(
        "ropecon2023.TimeSlot",
        verbose_name=_("When are you NOT able to host your programme?"),
        help_text=_(
            "Select the times when you are <b>NOT able</b> to run your larp. In other words, leave the times that you would be able to run your larp unselected!<br/>If you have a more specific request in mind regarding your schedule (for example, you would like to run your larp late at night), please let us know in the Comments section below.<br/>In this section, we would like to know more about how work or volunteer shifts, public transport schedules and other factors might be impacting your schedule. For example, if you need to leave the venue by 11pm to be able to catch the last bus to your accommodation."
        ),
        blank=True,
        related_name="+",
    )
    ropecon2024_blocked_time_slots = models.ManyToManyField(
        "ropecon2024.TimeSlot",
        verbose_name=_("When are you NOT able to host your programme?"),
        help_text=_(
            "Select the times when you are <b>NOT able</b> to run your larp. In other words, leave the times that you would be able to run your larp unselected!<br/>If you have a more specific request in mind regarding your schedule (for example, you would like to run your larp late at night), please let us know in the Comments section below.<br/>In this section, we would like to know more about how work or volunteer shifts, public transport schedules and other factors might be impacting your schedule. For example, if you need to leave the venue by 11pm to be able to catch the last bus to your accommodation."
        ),
        blank=True,
        related_name="+",
    )
    ropecon2023_language = models.CharField(
        max_length=max(len(key) for (key, text) in ROPECON2023_LANGUAGE_CHOICES),
        choices=ROPECON2023_LANGUAGE_CHOICES,
        default=ROPECON2023_LANGUAGE_CHOICES[0][0],
        verbose_name=_("Choose the language used in your programme"),
        help_text=_(
            "Finnish - choose this, if only Finnish is spoken in your programme.<br/>English - choose this, if only English is spoken in your programme.<br/>Language-free - choose this, if no Finnish or English is necessary to participate in the programme (e.g. a workshop with picture instructions or a dance where one can follow what others are doing).<br/>Finnish or English - choose this, if you are okay with having your programme language based on what language the attendees speak. Please write your title and programme description in both languages."
        ),
        null=True,
    )
    ropecon2023_suitable_for_all_ages = models.BooleanField(
        default=False,
        verbose_name=_("Suitable for all ages"),
        help_text=_("If your programme is suitable for all ages, please tick this box."),
    )
    ropecon2023_aimed_at_children_under_13 = models.BooleanField(
        default=False,
        verbose_name=_("Aimed at children under 13"),
        help_text=_("If your programme is designed for attendees under the age of 13 years, please tick this box."),
    )
    ropecon2023_aimed_at_children_between_13_17 = models.BooleanField(
        default=False,
        verbose_name=_("Aimed at children between 13-17"),
        help_text=_("If your programme is designed for attendees between 13-17 years of age, please tick this box."),
    )
    ropecon2023_aimed_at_adult_attendees = models.BooleanField(
        default=False,
        verbose_name=_("Aimed at adult attendees"),
        help_text=_("If your programme is designed for adult attendees, please tick this box."),
    )
    ropecon2023_for_18_plus_only = models.BooleanField(
        default=False,
        verbose_name=_("For 18+ only"),
        help_text=_(
            "If your programme contains themes that require attendees to be 18 years or older, please tick this box. There will be an ID check for all attendees."
        ),
    )
    ropecon2023_beginner_friendly = models.BooleanField(
        verbose_name=_("Beginner-friendly"),
        help_text=_(
            "If your programme is suitable for attendees with very limited knowledge or without any previous experience about the programme or subject matter in question, please tick this box."
        ),
        default=False,
    )
    ropecon2023_celebratory_year = models.BooleanField(
        verbose_name=_("Celebratory Year"),
        help_text=_("Check this box, if your programme is related to Ropecon's 30th celebratory year."),
        default=False,
    )
    ropecon2023_accessibility_cant_use_mic = models.BooleanField(
        default=False,
        verbose_name=_("I can't use a microphone"),
    )
    ropecon2023_accessibility_programme_duration_over_2_hours = models.BooleanField(
        default=False,
        verbose_name=_("The duration of the programme is over two hours without breaks."),
    )
    ropecon2023_accessibility_limited_opportunities_to_move_around = models.BooleanField(
        default=False,
        verbose_name=_("There are limited opportunities to move around during the programme."),
    )
    ropecon2023_accessibility_long_texts = models.BooleanField(
        default=False,
        verbose_name=_("Participation involves reading long texts independently"),
    )
    ropecon2023_accessibility_texts_not_available_as_recordings = models.BooleanField(
        default=False,
        verbose_name=_(
            "The programme includes texts that are essential to participation, and the texts are not available as recordings or read out loud."
        ),
    )
    ropecon2023_accessibility_participation_requires_dexterity = models.BooleanField(
        default=False,
        verbose_name=_("Participation requires some dexterity, e.g. that of hands and fingers."),
    )
    ropecon2023_accessibility_participation_requires_react_quickly = models.BooleanField(
        default=False,
        verbose_name=_("Participation requires the ability to react quickly."),
    )
    ropecon2023_other_accessibility_information = models.TextField(
        verbose_name=_("Other accessibility information"),
        help_text=_(
            "In the open field, define if necessary what features of your programme may possibly limit or enable participation (e.g. if the programme is available in sign language)."
        ),
        blank=True,
        null=True,
        default="",
    )
    ropecon2023_tables = models.PositiveIntegerField(
        verbose_name=_("Number of tables"),
        help_text=_(
            "How much table space is needed for your game programme: how many tables in total?<br/>Table size is 70 cm x 200 cm."
        ),
        validators=[MinValueValidator(1), MaxValueValidator(99)],
        null=True,
        blank=True,
    )
    ropecon2023_chairs = models.PositiveIntegerField(
        verbose_name=_("Number of chairs"),
        help_text=_("How many chairs are needed for your game programme."),
        validators=[MinValueValidator(1), MaxValueValidator(99)],
        null=True,
        blank=True,
    )
    ropecon2023_signuplist = models.CharField(
        max_length=15,
        choices=ROPECON2023_SIGNUP_LIST_CHOICES,
        default=ROPECON2023_SIGNUP_LIST_CHOICES[0][0],
        verbose_name=_("Sign-up process"),
        help_text=_(
            "How will players sign up for your game programme?<br/>No sign-up - no sign-up is required to participate in the game programme.<br/>Sign-up via the Konsti app - the sign-up process for the game programme is done via the Konsti app during the event.<br/>Other sign-up process - if your game programme requires attendees to sign up beforehand and you prefer to handle it through some other means (e.g. at the Gaming Desk), please choose this option and describe the sign-up process in the Comments section below."
        ),
        null=True,
    )
    ropecon2023_workshop_fee = models.CharField(
        max_length=1023,
        blank=True,
        default="0€",
        verbose_name=_("Workshop fee"),
        help_text=_(
            "If participation in the workshop requires a material fee, write the amount here as accurately as possible (if already known at the time of application). If not known (or there is no fee of any type), write 0€. Remember to update the exact amount to Kompassi before the release of the programme guide!"
        ),
    )
    ropecon2023_material_needs = models.TextField(
        blank=True,
        default="",
        verbose_name=_("Material needs"),
        help_text=_(
            "If you need assistance from Ropecon in acquiring or loaning the materials, inform about your needs here. It can be for example pens and paper, flip chart, miniature parts, miniature paint, iron wire etc."
        ),
    )
    ropecon2023_tables_and_chairs = models.CharField(
        max_length=1023,
        blank=True,
        default="",
        verbose_name=_("Number of tables and chairs"),
        help_text=_("Inform us how many tables and chairs are needed in your workshop."),
    )
    ropecon2023_furniture_needs = models.TextField(
        blank=True,
        default="",
        verbose_name=_("Other space and furniture needs"),
        help_text=_(
            "Inform us here, if you need a specific kind of space (and/or furniture) for your workshop. For example if tables and chairs need to be moved for empty space in your workshop, because it is not possible to do so in every room."
        ),
    )
    ropecon2024_language = models.CharField(
        max_length=max(len(key) for (key, text) in ROPECON2024_LANGUAGE_CHOICES),
        choices=ROPECON2024_LANGUAGE_CHOICES,
        default=ROPECON2024_LANGUAGE_CHOICES[0][0],
        verbose_name=_("Choose the language used in your programme"),
        help_text=_(
            "Finnish - choose this, if only Finnish is spoken in your programme.<br><br>English - choose this, if only English is spoken in your programme.<br><br>Language-free - choose this, if no Finnish or English is necessary to participate in the programme (e.g. a workshop with picture instructions or a dance where one can follow what others are doing).<br><br>Finnish or English - choose this, if you are okay with either of the two languages. The programme team will contact you regarding the final choice of language.<br><br>Finnish and English - choose this, if your programme item will use both Finnish and English (e.g. if you will switch languages based on participants).<br><br>Other - choose this, if your programme is in a language other than Finnish or English. If chosen, please provide the title and description of your programme in the chosen language."
        ),
        null=True,
    )
    ropecon2024_language_other = models.CharField(
        max_length=1023,
        blank=True,
        default="",
        verbose_name=_("Other"),
        help_text=_('If you chose "other", enter the language or languages you will be using in your programme here'),
    )
    is_using_paikkala = models.BooleanField(
        default=False,
        verbose_name=_("Reservable seats"),
        help_text=_("If selected, reserved seats for this programme will be offered."),
    )
    paikkala_program = models.OneToOneField(
        "paikkala.Program",
        on_delete=models.SET_NULL,
        null=True,
        related_name="kompassi_programme",
    )
    paikkala_icon = models.FileField(
        upload_to="paikkala_icons",
        blank=True,
        verbose_name=_("Programme icon"),
        help_text=_(
            "The programme icon is used to make it harder to mix up reservations of different programmes during inspection."
        ),
    )
    is_paikkala_public = models.BooleanField(
        default=True,
        verbose_name=_("Publicly reservable"),
        help_text=_(
            "If selected, this programme will be shown in listings as publicly reservable while it is in its reservation period. Non-publicly reservable programmes can only be accessed by knowing the direct URL."
        ),
    )
    is_paikkala_time_visible = models.BooleanField(
        default=True,
        verbose_name=_("Programme time is visible in Paikkala context"),
        help_text=_(
            "If selected, the time of this progrmme will be shown in reservation context. This is used to hide the time in contexts in which the time is not relevant or would be misleading, particularly Tracon afterparty coaches."
        ),
    )

    ropecon2018_audience_size = models.CharField(
        default="unknown",
        null=True,
        choices=ROPECON2018_AUDIENCE_SIZE_CHOICES,
        max_length=max(len(key) for (key, label) in ROPECON2018_AUDIENCE_SIZE_CHOICES),
        verbose_name=_("Audience estimate"),
        help_text=_("Estimate of audience size for talk/presentation, if you have previous experience."),
    )

    ropecon2018_is_no_language = models.BooleanField(
        verbose_name=_("No language"),
        help_text=_("No Finnish language needed to participate."),
        default=False,
    )

    ropecon2018_is_panel_attendance_ok = models.BooleanField(
        verbose_name=_("Panel talk"),
        help_text=_("I can participate in a panel discussion related to my field of expertise."),
        default=False,
    )

    ropecon2018_speciality = models.CharField(
        verbose_name=_("My field(s) of expertise"),
        max_length=100,
        blank=True,
        null=True,
        default="",
    )

    ropecon2018_genre_fantasy = models.BooleanField(
        verbose_name=_("Fantasy"),
        default=False,
    )

    ropecon2018_genre_scifi = models.BooleanField(
        verbose_name=_("Sci-fi"),
        default=False,
    )

    ropecon2018_genre_historical = models.BooleanField(
        verbose_name=_("Historical"),
        default=False,
    )

    ropecon2018_genre_modern = models.BooleanField(
        verbose_name=_("Modern"),
        default=False,
    )

    ropecon2018_genre_war = models.BooleanField(
        verbose_name=_("War"),
        default=False,
    )

    ropecon2018_genre_horror = models.BooleanField(
        verbose_name=_("Horror"),
        default=False,
    )

    ropecon2018_genre_exploration = models.BooleanField(
        verbose_name=_("Exploration"),
        default=False,
    )

    ropecon2019_genre_adventure = models.BooleanField(
        verbose_name=_("Adventure"),
        default=False,
    )

    ropecon2018_genre_mystery = models.BooleanField(
        verbose_name=_("Mystery"),
        default=False,
    )

    ropecon2018_genre_drama = models.BooleanField(
        verbose_name=_("Drama"),
        default=False,
    )

    ropecon2018_genre_humor = models.BooleanField(
        verbose_name=_("Humor"),
        default=False,
    )

    ropecon2018_style_serious = models.BooleanField(
        verbose_name=_("Serious game style"),
        default=False,
    )

    ropecon2018_style_light = models.BooleanField(
        verbose_name=_("Light game style"),
        default=False,
    )

    ropecon2018_style_rules_heavy = models.BooleanField(
        verbose_name=_("Rules heavy"),
        default=False,
    )

    ropecon2018_style_rules_light = models.BooleanField(
        verbose_name=_("Rules light"),
        default=False,
    )

    ropecon2018_style_story_driven = models.BooleanField(
        verbose_name=_("Story driven"),
        default=False,
    )

    ropecon2018_style_character_driven = models.BooleanField(
        verbose_name=_("Character driven"),
        default=False,
    )

    ropecon2018_style_combat_driven = models.BooleanField(
        verbose_name=_("Combat driven"),
        default=False,
    )

    ropecon2018_sessions = models.PositiveIntegerField(
        verbose_name=_("number of times you want to run the game"),
        help_text=_(
            "Please let us know your preference. Due to the limited space we are not able to accommodate all requests. One four hour session gives you one weekend ticket. A second session gives you an additional day ticket."
        ),
        default=2,
        validators=[MinValueValidator(1), MaxValueValidator(999)],
        null=True,
    )

    ropecon2018_characters = models.PositiveIntegerField(
        verbose_name=_("number of characters"),
        help_text=_("If the game design requires characters with a specific gender let us know in the notes."),
        default=10,
        validators=[MinValueValidator(1), MaxValueValidator(999)],
        null=True,
    )

    ropecon2018_signuplist = models.CharField(
        max_length=15,
        choices=ROPECON2018_SIGNUP_LIST_CHOICES,
        default=ROPECON2018_SIGNUP_LIST_CHOICES[0][0],
        verbose_name=_("Will you make your own signup sheet"),
        help_text=_(
            "A self-made signup sheet allows you to ask more detailed player preferences. Larp-desk-made signup sheet is a list of participant names."
        ),
        null=True,
    )

    ropecon2018_space_requirements = models.TextField(
        verbose_name=_("Space and technical requirements"),
        help_text=_(
            "Let us know of your requirements. Fully dark, separate rooms, water outlet, sound, light, etc. Not all requests can be accommodated so please explain how your request improves the game."
        ),
        blank=True,
        null=True,
        default="",
    )

    ropecon2018_prop_requirements = models.CharField(
        verbose_name=_("Prop requirements"),
        help_text=_(
            "Let us know what props and other equipment you need and if you can provide some of them yourself. Not all requests can be accommodated. Water and glasses are always provided."
        ),
        max_length=200,
        blank=True,
        null=True,
        default="",
    )

    ropecon2018_kp_length = models.CharField(
        max_length=2,
        choices=ROPECON2018_KP_LENGTH_CHOICES,
        default=ROPECON2018_KP_LENGTH_CHOICES[0][0],
        verbose_name=_("How long do you present your game"),
        help_text=_("Presenters get a weekend ticket for 8 hours of presenting or a day ticket for 4 hours."),
        null=True,
    )

    ropecon2018_kp_difficulty = models.CharField(
        max_length=15,
        choices=ROPECON2018_KP_DIFFICULTY_CHOICES,
        default=ROPECON2018_KP_DIFFICULTY_CHOICES[0][0],
        verbose_name=_("Game difficulty and complexity"),
        null=True,
    )

    ropecon2018_kp_tables = models.CharField(
        max_length=5,
        choices=ROPECON2018_KP_TABLE_COUNT_CHOICES,
        default=ROPECON2018_KP_TABLE_COUNT_CHOICES[0][0],
        verbose_name=_("How many tables do you need"),
        help_text=_("Table size is about 140 x 80 cm."),
        null=True,
    )

    ropecon2021_gamedesk_physical_or_virtual = models.CharField(
        max_length=max(len(key) for (key, text) in ROPECON2021_GAMEDESK_PHYSICAL_OR_VIRTUAL_CHOICES),
        choices=ROPECON2021_GAMEDESK_PHYSICAL_OR_VIRTUAL_CHOICES,
        default=ROPECON2021_GAMEDESK_PHYSICAL_OR_VIRTUAL_CHOICES[0][0],
        verbose_name=_("Physical or virtual programme?"),
        help_text=_(
            "The organizers of Ropecon strive to organize a physical con, and if the con can be held thusly, virtual programmes will not be organized. If the con cannot be face to face, we cannot organize physical programmes during a virtual con.<br><br>Specify here whether your programme can be organized face to face, virtually, or either way."
        ),
        null=True,
    )

    ropecon2021_larp_physical_or_virtual = models.CharField(
        max_length=max(len(key) for (key, text) in ROPECON2021_LARP_PHYSICAL_OR_VIRTUAL_CHOICES),
        choices=ROPECON2021_LARP_PHYSICAL_OR_VIRTUAL_CHOICES,
        default=ROPECON2021_LARP_PHYSICAL_OR_VIRTUAL_CHOICES[0][0],
        verbose_name=_("I am submitting a larp for"),
        help_text=_("Select the event form appropriate for the larp you have planned."),
        null=True,
    )

    solmukohta2024_ticket = models.BooleanField(
        default=False,
        verbose_name=_("I have purchased or am about to purchase a Solmukohta 2024 ticket"),
        help_text=_(
            "I understand that if my programme item is accepted, I will still need to purchase "
            "a Solmukohta 2024 ticket in order to attend."
        ),
    )

    solmukohta2024_content_warnings = models.ManyToManyField(
        "solmukohta2024.ContentWarning",
        blank=True,
        verbose_name=_("The programme item contains..."),
        help_text=_(
            'Please check all that apply; if there are other potential content warnings, add them under "other".'
        ),
    )

    solmukohta2024_technology = models.ManyToManyField(
        "solmukohta2024.Technology",
        blank=True,
        verbose_name=_("Technical needs"),
    )

    solmukohta2024_other_needs = models.TextField(
        blank=True,
        default="",
        verbose_name=_("Other needs"),
        help_text=_(
            "Please enter any other needs here, such as paper and markers for a workshop, spatial needs for a larp, etc. Also mention here if you want to have your programme item outside, in the pool, or in an otherwise unusual environment."
        ),
    )

    solmukohta2024_documentation = models.ManyToManyField(
        "solmukohta2024.Documentation",
        blank=True,
        verbose_name="Documentation",
        help_text=_("Check all that apply; you can learn more about these options in the Hosting Guide."),
    )

    solmukohta2024_scheduling = models.TextField(
        blank=True,
        default="",
        verbose_name=_("Scheduling restrictions"),
        help_text=_(
            "Please tell us if there are any restrictions to scheduling your programme item (if you will be arriving late or leaving early or the like)."
        ),
    )

    solmukohta2024_panel_participation = models.ManyToManyField(
        "solmukohta2024.PanelParticipation",
        blank=True,
        verbose_name=_("Panel participation"),
    )

    solmukohta2024_areas_of_expertise = models.TextField(
        blank=True,
        default="",
        verbose_name=_("Areas of expertise"),
        help_text=_("Please fill this in only if you checked the Panel participation box above"),
    )

    solmukohta2024_have_you_hosted_before = models.CharField(
        blank=True,
        max_length=max(len(key) for (key, text) in SOLMUKOHTA2024_HAVE_YOU_HOSTED_BEFORE_CHOICES),
        choices=SOLMUKOHTA2024_HAVE_YOU_HOSTED_BEFORE_CHOICES,
        default="",
        verbose_name=_("Have you hosted program for SK/KP before?"),
    )

    solmukohta2024_mentoring = models.ManyToManyField(
        "solmukohta2024.Mentoring",
        blank=True,
        verbose_name=_("Mentoring"),
        help_text=_(
            "Less experienced presenters who would like some guidance may request a mentor. "
            "More experienced presenters can volunteer here to help. (This usually involves a "
            "few emails or Skype calls 1-2 months leading up to the event.)"
        ),
    )

    solmukohta2024_other_emails = models.CharField(
        max_length=1023,
        blank=True,
        default="",
        verbose_name=_("Email addresses of other programme hosts"),
        help_text=_(
            "We will make a mailing list to reach all our programme hosts for the purpose of keeping you informed. "
            "You need not add your own email address here – it will be shared with us when you submit this form."
        ),
    )

    aweek2024_when = models.TextField(
        blank=True,
        default="",
        verbose_name=_("When would you like to run your programme?"),
        help_text=_(
            "A Week-in is happening from Monday to Wednesday. "
            "Check above the available times at the main location Artteli. "
            "Please include your preparation time on the location as well, "
            "if your programme item is happening at Artteli. "
            "We do our best to make things not overlap!"
        ),
    )

    aweek2024_participants = models.CharField(
        max_length=1023,
        blank=True,
        default="",
        verbose_name=_("For how many people your program item is for?"),
    )

    aweek2024_signup = models.CharField(
        max_length=1023,
        blank=True,
        default="",
        verbose_name=_("Sign-up requirements"),
        help_text=_("Does your program item need sign-up or is it free for everyone to attend?"),
    )

    aweek2024_prepare = models.CharField(
        max_length=1023,
        blank=True,
        default="",
        verbose_name=_("Preparations required"),
        help_text=_("Do the participants need to prepare somehow?"),
    )

    other_author = models.CharField(
        max_length=1023,
        blank=True,
        default="",
        verbose_name=_("Author (if other than the GM)"),
        help_text=_(
            "If the scenario has been written by someone else than the GM, we require that the author be disclosed."
        ),
    )

    content_warnings = models.CharField(
        max_length=1023,
        blank=True,
        default="",
        verbose_name=_("Content warnings"),
        help_text=_("If your program contains heavy topics or potentially distressing themes, please mention it here."),
    )

    # Internal fields
    notes = models.TextField(
        blank=True,
        verbose_name=_("Internal notes"),
        help_text=_(
            "This field is normally only visible to the programme managers. However, should the programme "
            "host request a record of their own personal details, this field will be included in that record."
        ),
    )
    room = models.ForeignKey(
        "programme.Room",
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        verbose_name=_("Room"),
        related_name="programmes",
    )
    organizers = models.ManyToManyField("core.Person", through="ProgrammeRole", blank=True)
    tags = models.ManyToManyField("programme.Tag", blank=True, verbose_name=_("Tags"))

    video_link = models.CharField(
        max_length=255,
        blank=True,
        default="",
        verbose_name=_("Video link"),
        help_text=_("A link to a recording of the programme in an external video service such as YouTube"),
    )
    signup_link = models.CharField(
        max_length=255,
        blank=True,
        default="",
        verbose_name=_("Signup link"),
        help_text=_(
            "If the programme requires signing up in advance, put a link here and it will be shown "
            "as a button in the schedule."
        ),
    )

    created_at = models.DateTimeField(auto_now_add=True, null=True, verbose_name=_("Created at"))
    updated_at = models.DateTimeField(auto_now=True, null=True, verbose_name=_("Updated at"))

    @property
    def event(self):
        return self.category.event

    @property
    def programme_roles(self):
        from .programme_role import ProgrammeRole

        return ProgrammeRole.objects.filter(programme=self)

    @cached_property
    def formatted_hosts(self):
        from .freeform_organizer import FreeformOrganizer

        if self.hosts_from_host:
            return self.hosts_from_host

        parts = [f.text for f in FreeformOrganizer.objects.filter(programme=self)]

        public_programme_roles = self.programme_roles.filter(role__is_public=True).select_related("person")

        parts.extend(pr.person.display_name for pr in public_programme_roles)

        return ", ".join(parts)

    @property
    def is_blank(self):
        return False

    def __str__(self):
        return self.title

    @property
    def css_classes(self):
        return self.category.style if self.category.style else ""

    @property
    def is_active(self):
        return self.state in PROGRAMME_STATES_ACTIVE

    @property
    def is_rejected(self):
        return self.state == "rejected"

    @property
    def is_cancelled(self):
        return self.state == "cancelled"

    @property
    def is_published(self):
        return self.state == "published"

    is_open_for_feedback = False

    @property
    def show_signup_link(self):
        t = now()
        return self.signup_link and (
            (self.start_time is not None and t <= self.start_time)
            or (self.event.start_time is not None and t <= self.event.start_time)
        )

    @classmethod
    def get_or_create_dummy(
        cls,
        title="Dummy program",
        state="published",
        event: Event | None = None,
    ):
        from .category import Category
        from .room import Room

        category, unused = Category.get_or_create_dummy(event=event)
        room, unused = Room.get_or_create_dummy(event=event)

        return cls.objects.get_or_create(
            title=title,
            defaults=dict(
                category=category,
                room=room,
                state=state,
            ),
        )

    @property
    def formatted_start_time(self):
        return format_datetime(self.start_time) if self.start_time else ""

    @property
    def formatted_times(self):
        return format_interval(self.start_time, self.end_time)

    # for json
    @property
    def category_title(self):
        return self.category.title

    @property
    def room_name(self):
        return self.room.name if self.room is not None else None

    @property
    def is_public(self):
        return self.state == "published" and self.category is not None and self.category.public

    @property
    def public_tags(self):
        return self.tags.filter(public=True)

    def as_json(self, format="default"):
        from core.utils import pick_attrs

        if format == "default":
            return pick_attrs(
                self,
                "title",
                "description",
                "category_title",
                "formatted_hosts",
                "room_name",
                "length",
                "start_time",
                "is_public",
                "video_link",
            )
        elif format == "desucon":
            return pick_attrs(
                self,
                "title",
                "description",
                "start_time",
                "end_time",
                "language",
                "video_link",
                status=1 if self.is_public else 0,
                kind=self.category.slug,
                kind_display=self.category.title,
                identifier=self.slug or f"p{self.id}",
                location=self.room.name if self.room else None,
                location_slug=self.room.slug if self.room else None,
                presenter=self.formatted_hosts,
                tags=list(self.tags.values_list("slug", flat=True)),
            )
        elif format == "ropecon":
            return pick_attrs(
                self,
                "title",
                "description",
                "category_title",
                "formatted_hosts",
                "room_name",
                "length",
                "start_time",
                "end_time",
                "rpg_system",
                other_author=self.other_author if self.category.slug == "larp" else None,
                min_players=self.min_players,
                max_players=self.max_players,
                ropecon2018_characters=self.ropecon2018_characters if self.category.slug == "larp" else None,
                ropecon2023_signuplist=self.ropecon2023_signuplist
                if self.form_used and self.form_used.slug == "pelitiski"
                else None,
                ropecon2023_workshop_fee=self.ropecon2023_workshop_fee
                if self.form_used and self.form_used.slug == "tyopaja"
                else None,
                identifier=f"p{self.id}",
                tags=list(self.tags.values_list("slug", flat=True)),
                ropecon2023_language=self.ropecon2023_language,
                ropecon2023_suitable_for_all_ages=self.ropecon2023_suitable_for_all_ages,
                ropecon2023_aimed_at_children_under_13=self.ropecon2023_aimed_at_children_under_13,
                ropecon2023_aimed_at_children_between_13_17=self.ropecon2023_aimed_at_children_between_13_17,
                ropecon2023_aimed_at_adult_attendees=self.ropecon2023_aimed_at_adult_attendees,
                ropecon2023_for_18_plus_only=self.ropecon2023_for_18_plus_only,
                ropecon2023_beginner_friendly=self.ropecon2023_beginner_friendly,
                ropecon_theme=self.ropecon_theme,
                ropecon2023_celebratory_year=self.ropecon2023_celebratory_year,
                styles=self.ropecon_styles,
                revolving_door=self.is_revolving_door if self.category.slug == "rpg" else None,
                short_blurb=self.three_word_description if self.category.slug in ("rpg", "larp") else None,
                ropecon2023_accessibility_cant_use_mic=self.ropecon2023_accessibility_cant_use_mic,
                ropecon2021_accessibility_loud_sounds=self.ropecon2021_accessibility_loud_sounds,
                ropecon2021_accessibility_flashing_lights=self.ropecon2021_accessibility_flashing_lights,
                ropecon2021_accessibility_strong_smells=self.ropecon2021_accessibility_strong_smells,
                ropecon2021_accessibility_irritate_skin=self.ropecon2021_accessibility_irritate_skin,
                ropecon2021_accessibility_physical_contact=self.ropecon2021_accessibility_physical_contact,
                ropecon2021_accessibility_low_lightning=self.ropecon2021_accessibility_low_lightning,
                ropecon2021_accessibility_moving_around=self.ropecon2021_accessibility_moving_around,
                ropecon2023_accessibility_programme_duration_over_2_hours=self.ropecon2023_accessibility_programme_duration_over_2_hours,
                ropecon2023_accessibility_limited_opportunities_to_move_around=self.ropecon2023_accessibility_limited_opportunities_to_move_around,
                ropecon2021_accessibility_video=self.ropecon2021_accessibility_video,
                ropecon2021_accessibility_recording=self.ropecon2021_accessibility_recording,
                ropecon2023_accessibility_long_texts=self.ropecon2023_accessibility_long_texts,
                ropecon2023_accessibility_texts_not_available_as_recordings=self.ropecon2023_accessibility_texts_not_available_as_recordings,
                ropecon2023_accessibility_participation_requires_dexterity=self.ropecon2023_accessibility_participation_requires_dexterity,
                ropecon2023_accessibility_participation_requires_react_quickly=self.ropecon2023_accessibility_participation_requires_react_quickly,
                ropecon2021_accessibility_colourblind=self.ropecon2021_accessibility_colourblind,
                ropecon2022_content_warnings=self.ropecon2022_content_warnings,
                ropecon2023_other_accessibility_information=self.ropecon2023_other_accessibility_information,
            )
        elif format == "hitpoint":
            return pick_attrs(
                self,
                "title",
                "description",
                "category_title",
                "formatted_hosts",
                "room_name",
                "length",
                "start_time",
                "is_public",
                "video_link",
                "min_players",
                "max_players",
                "three_word_description",
                "physical_play",
                "other_author",
                "is_english_ok",
                "is_age_restricted",
                "is_beginner_friendly",
                "rpg_system",
                "is_children_friendly",
                "is_intended_for_experienced_participants",
                identifier=f"p{self.id}",
            )
        else:
            raise NotImplementedError(format)

    @property
    def ropecon_genres(self):
        found_genres = []

        for prefix, possible_genres in [
            (
                "ropecon2018",
                [
                    "fantasy",
                    "scifi",
                    "historical",
                    "modern",
                    "war",
                    "horror",
                    "exploration",
                    "mystery",
                    "drama",
                    "humor",
                ],
            ),
            ("ropecon2019", ["adventure"]),
        ]:
            for genre in possible_genres:
                if getattr(self, f"{prefix}_genre_{genre}"):
                    found_genres.append(genre)

        return found_genres

    @property
    def ropecon_styles(self):
        styles = []

        for style in [
            "serious",
            "light",
            "rules_heavy",
            "rules_light",
            "story_driven",
            "character_driven",
            "combat_driven",
        ]:
            if getattr(self, "ropecon2018_style_" + style):
                styles.append(style)

        return styles

    @property
    def state_css(self):
        return STATE_CSS[self.state]

    @property
    def signup_extras(self):
        SignupExtra = self.event.programme_event_meta.signup_extra_model

        if SignupExtra and SignupExtra.supports_programme:
            return SignupExtra.objects.filter(event=self.event, person__in=self.organizers.all())
        else:
            return SignupExtra.objects.none()

    def save(self, *args, **kwargs):
        if self.start_time and self.length:
            self.end_time = self.start_time + timedelta(minutes=self.length)

        if self.title and not self.slug:
            slug = base_slug = slugify(self.title)
            counter = 1

            qs = Programme.objects.filter(category__event=self.category.event)
            if self.pk:
                qs = qs.exclude(pk=self.pk)

            while qs.filter(slug=slug).exists():
                counter += 1
                slug = f"{base_slug}-{counter}"

            self.slug = slug

        return super().save(*args, **kwargs)

    def apply_state(self, deleted_programme_roles=None):
        if deleted_programme_roles is None:
            deleted_programme_roles = []
        self.apply_state_sync(deleted_programme_roles)
        self.apply_state_async()

    def apply_state_sync(self, deleted_programme_roles):
        self.paikkalize()
        self.apply_state_update_programme_roles()
        self.apply_state_update_signup_extras()
        self.apply_state_create_badges(deleted_programme_roles)

    def apply_state_async(self):
        from ..tasks import programme_apply_state_async

        programme_apply_state_async.delay(self.pk)  # type: ignore

    def _apply_state_async(self):
        self.apply_state_group_membership()
        self.apply_state_send_messages()

    def apply_state_update_programme_roles(self):
        self.programme_roles.update(is_active=self.is_active)

    def apply_state_update_signup_extras(self):
        for signup_extra in self.signup_extras:
            signup_extra.apply_state()

    def apply_state_group_membership(self):
        from core.utils import ensure_user_group_membership

        from .alternative_programme_form import AlternativeProgrammeForm
        from .category import Category
        from .programme_role import ProgrammeRole

        for person in self.organizers.all():
            if not person.user:
                raise ValueError(f"{person=} has no associated user")

            groups_to_add = []
            groups_to_remove = []

            # Status based groups
            for group, states in [
                (self.event.programme_event_meta.get_group_if_exists("new"), PROGRAMME_STATES_NEW),
                (self.event.programme_event_meta.get_group_if_exists("hosts"), PROGRAMME_STATES_ACTIVE),
                (self.event.programme_event_meta.get_group_if_exists("live"), PROGRAMME_STATES_LIVE),
                (self.event.programme_event_meta.get_group_if_exists("inactive"), PROGRAMME_STATES_INACTIVE),
            ]:
                if not group:
                    continue

                if ProgrammeRole.objects.filter(
                    programme__category__event=self.event,
                    programme__state__in=states,
                    person=person,
                ).exists():
                    # active programmist
                    groups_to_add.append(group)
                else:
                    # inactive programmist
                    groups_to_remove.append(group)

            # Category groups
            for category in Category.objects.filter(event=self.event):
                group = self.event.programme_event_meta.get_group_if_exists(category.qualified_slug)
                if not group:
                    continue

                if ProgrammeRole.objects.filter(
                    programme__category=category,
                    programme__state__in=PROGRAMME_STATES_LIVE,
                    person=person,
                ).exists():
                    # active programmist
                    groups_to_add.append(group)
                else:
                    # inactive programmist
                    groups_to_remove.append(group)

            # Form groups
            for form in AlternativeProgrammeForm.objects.filter(event=self.event):
                group = self.event.programme_event_meta.get_group_if_exists(form.qualified_slug)
                if not group:
                    continue

                if ProgrammeRole.objects.filter(
                    programme__form_used=form,
                    programme__state__in=PROGRAMME_STATES_LIVE,
                    person=person,
                ).exists():
                    # active programmist
                    groups_to_add.append(group)
                else:
                    # inactive programmist
                    groups_to_remove.append(group)

            ensure_user_group_membership(person.user, groups_to_add=groups_to_add, groups_to_remove=groups_to_remove)

    def apply_state_send_messages(self, resend=False):
        from mailings.models import Message

        for person in self.organizers.all():
            Message.send_messages(self.event, "programme", person)

    def apply_state_create_badges(self, deleted_programme_roles=None):
        if deleted_programme_roles is None:
            deleted_programme_roles = []
        if "badges" not in settings.INSTALLED_APPS:
            return

        if self.event.badges_event_meta is None:
            return

        from badges.models import Badge

        for person in self.organizers.all():
            Badge.ensure(event=self.event, person=person)

        for deleted_programme_role in deleted_programme_roles:
            Badge.ensure(event=self.event, person=deleted_programme_role.person)

    @classmethod
    def _get_in_states(cls, person, states, q=None, **extra_criteria):
        """
        Get me the programmes of this person which are in these states. Oh and I might have
        some extra requirements for the programmes in the form of a Q object or kwargs.
        """

        if q is None:
            q = Q()

        q = q & Q(state__in=states, organizers=person)

        if extra_criteria:
            q = q & Q(**extra_criteria)

        return cls.objects.filter(q).distinct().order_by("category__event__start_time", "start_time", "title")

    @classmethod
    def get_future_programmes(cls, person, t=None):
        if t is None:
            t = now()

        return cls._get_in_states(
            person,
            PROGRAMME_STATES_ACTIVE,
            Q(end_time__gt=t) | Q(end_time__isnull=True) & Q(category__event__end_time__gt=t),
        )

    @classmethod
    def get_past_programmes(cls, person, t=None):
        if t is None:
            t = now()

        return cls._get_in_states(
            person,
            PROGRAMME_STATES_ACTIVE,
            Q(end_time__lte=t) | Q(end_time__isnull=True) & Q(category__event__end_time__lte=t),
        )

    @classmethod
    def get_rejected_programmes(cls, person):
        return cls._get_in_states(person, PROGRAMME_STATES_INACTIVE)

    @property
    def host_can_edit(self):
        return (
            self.state in PROGRAMME_STATES_ACTIVE
            and not self.frozen
            and not (self.event.end_time and now() >= self.event.end_time)
        )

    @property
    def host_cannot_edit_explanation(self):
        assert not self.host_can_edit  # noqa: S101

        if self.state == "cancelled":
            return _("You have cancelled this programme.")
        elif self.state == "rejected":
            return _("This programme has been rejected by the programme manager.")
        elif self.frozen:
            return _("This programme has been frozen by the programme manager.")
        elif now() >= self.event.end_time:
            return _("The event has ended and the programme has been archived.")
        else:
            raise NotImplementedError(self.state)

    def get_feedback_url(self, request=None):
        path = url("programme:feedback_view", self.event.slug, self.pk)

        if request:
            return request.build_absolute_uri(path)
        else:
            return path

    @property
    def visible_feedback(self):
        return self.feedback.filter(hidden_at__isnull=True).select_related("author").order_by("-created_at")

    @property
    def can_paikkalize(self):
        return (
            self.room is not None
            and self.room.has_paikkala_schema
            and self.start_time is not None
            and self.length is not None
        )

    @atomic
    def paikkalize(self, **paikkalkwargs):
        if not self.is_using_paikkala:
            return None
        if self.paikkala_program:
            return self.paikkala_program

        if not self.can_paikkalize:
            raise AssertionError("self.can_paikkalize")

        from django.template.defaultfilters import truncatechars
        from paikkala.models import Program as PaikkalaProgram
        from paikkala.models import Row

        paikkala_room = self.room.paikkalize()  # type: ignore
        meta = self.event.programme_event_meta
        tz = get_default_timezone()

        paikkala_program_kwargs = dict(
            event_name=self.event.name,
            name=truncatechars(self.title, PaikkalaProgram._meta.get_field("name").max_length),  # type: ignore
            room=paikkala_room,
            require_user=True,
            reservation_start=self.start_time.replace(hour=9, minute=0, tzinfo=tz),  # type: ignore
            reservation_end=self.end_time,
            invalid_after=self.end_time,
            max_tickets=0,
            automatic_max_tickets=True,
            max_tickets_per_user=meta.paikkala_default_max_tickets_per_user,
            max_tickets_per_batch=meta.paikkala_default_max_tickets_per_batch,
        )
        paikkala_program_kwargs.update(paikkalkwargs)

        self.paikkala_program = PaikkalaProgram.objects.create(**paikkala_program_kwargs)

        self.save()

        self.paikkala_program.rows.set(Row.objects.filter(zone__room=paikkala_room))
        self.paikkala_program.full_clean()
        self.paikkala_program.save()

        return self.paikkala_program

    @property
    def is_open_for_seat_reservations(self):
        return self.is_using_paikkala and self.paikkala_program and self.paikkala_program.is_reservable

    def get_csv_fields(self, event):
        fields = super().get_csv_fields(event)
        return [
            (cls, field)
            for (cls, field) in fields
            if (
                field not in CSV_EXPORT_EXCLUDED_FIELDS
                and getattr(field, "name", None) not in CSV_EXPORT_EXCLUDED_FIELDS
            )
        ]

    class Meta:
        verbose_name = _("programme")
        verbose_name_plural = _("programmes")
        ordering = ["start_time", "room"]
        indexes = [
            models.Index(fields=["category", "state"]),
            models.Index(fields=["category", "slug"]),
        ]
