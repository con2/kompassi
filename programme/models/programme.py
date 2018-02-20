import logging
from datetime import timedelta

from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import Q
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _


from core.csv_export import CsvExportMixin
from core.utils import (
    format_datetime,
    NONUNIQUE_SLUG_FIELD_PARAMS,
    slugify,
    url,
)


logger = logging.getLogger('kompassi')


VIDEO_PERMISSION_CHOICES = [
    ('public', _('My programme may be recorded and published')),
    ('private', _('I forbid publishing my programme, but it may be recorded for archiving purposes')),
    ('forbidden', _('I forbid recording my programme altogether')),
]
START_TIME_LABEL = _('Starting time')

STATE_CHOICES = [
    ('idea', _('Internal programme idea')),
    ('asked', _('Asked from the host')),
    ('offered', _('Offer received')),
    ('accepted', _('Accepted')),
    ('published', _('Published')),

    ('cancelled', _('Cancelled')),
    ('rejected', _('Rejected')),
]

STATE_CSS = dict(
    idea='label-default',
    asked='label-default',
    offered='label-default',

    accepted='label-primary',
    published='label-success',

    cancelled='label-danger',
    rejected='label-danger',
)

COMPUTER_CHOICES = [
    ('con', _('Laptop provided by the event')),
    ('pc', _('Own laptop – PC')),
    ('mac', _('Own laptop – Mac')),
    ('none', _('No computer required')),
]

TRISTATE_CHOICES = [
    ('yes', _('Yes')),
    ('no', _('No')),
    ('notsure', _('Not sure')),
]

TRISTATE_FIELD_PARAMS = dict(
    choices=TRISTATE_CHOICES,
    max_length=max(len(key) for (key, label) in TRISTATE_CHOICES),
)

ENCUMBERED_CONTENT_CHOICES = [
    ('yes', _('My programme contains copyright-encumbered audio or video')),
    ('no', _('My programme does not contain copyright-encumbered audio or video')),
    ('notsure', _('I\'m not sure whether my programme contains copyright-encumbered content or not')),
]

PHOTOGRAPHY_CHOICES = [
    ('please', _('Please photograph my programme')),
    ('okay', _('It\'s OK to photograph my programme')),
    ('nope', _('Please do not photograph my programme')),
]

RERUN_CHOICES = [
    ('already', _('Yes. The programme has previously been presented in another convention.')),
    ('will', _('Yes. The programme will be presented in a convention that takes place before this one.')),
    ('might', _('Maybe. The programme might be presented in a convention that takes place before this one.')),
    ('original', _(
        'No. The programme is original to this convention and I promise not to present it elsewhere before.'
    )),
]

PHYSICAL_PLAY_CHOICES = [
    ('lots', _('Lots of it')),
    ('some', _('Some')),
    ('none', _('Not at all')),
]

PROGRAMME_STATES_ACTIVE = ['idea', 'asked', 'offered', 'accepted', 'published']
PROGRAMME_STATES_INACTIVE = ['rejected', 'cancelled']


class Programme(models.Model, CsvExportMixin):
    """
    Represents a scheduled programme in an event. Usually belongs to a Category and has a start and
    end time. Also usually happens in a Room.

    Note that this is a "dense sparse model" meaning the model covers multiple types of Programme
    some of which have fields that are not used by the others. The fields used are specified by the
    Form used. The default form fits lectures etc. and other types of programme are covered using
    AlternativeProgrammeForms.
    """

    category = models.ForeignKey('programme.Category',
        verbose_name=_('category'),
        help_text=_('Choose the category that fits your programme the best. We reserve the right to change this.'),
    )
    form_used = models.ForeignKey('programme.AlternativeProgrammeForm',
        blank=True,
        null=True,
        verbose_name=_('form used'),
        help_text=_('Which form was used to offer this Programme? If null, the default form was used.'),
    )

    slug = models.CharField(**NONUNIQUE_SLUG_FIELD_PARAMS)

    title = models.CharField(
        max_length=1023,
        verbose_name=_('Title'),
        help_text=_('Make up a concise title for your programme. We reserve the right to edit the title.'),
    )

    description = models.TextField(
        blank=True,
        default='',
        verbose_name=_('Description'),
        help_text=_(
            'This description is published in the web schedule and the programme booklet. The purpose of this '
            'description is to give the participant sufficient information to decide whether to take part or '
            'not and to market your programme to the participants. We reserve the right to edit the '
            'description.'
        ),
    )
    long_description = models.TextField(
        blank=True,
        default='',
        verbose_name='Tarkempi kuvaus',
        help_text=(
            'Kuvaile ohjelmaasi tarkemmin ohjelmavastaavalle. Minkälaista rakennetta olet ohjelmallesi '
            'suunnitellut? Millaisia asioita tulisit käsittelemään? Kerro myös onko ohjelmasi suunnattu '
            'aloittevammille vai kokeneemmille harrastajille.'
        ),
    )
    three_word_description = models.CharField(
        max_length=1023,
        blank=True,
        default='',
        verbose_name=_('Three-word description'),
        help_text=_('Describe your game in three words: for example, genre, theme and attitude.'),
    )

    use_audio = models.CharField(
        default='no',
        verbose_name=_('Audio playback'),
        help_text=_('Will you play audio in your programme?'),
        **TRISTATE_FIELD_PARAMS
    )

    use_video = models.CharField(
        default='no',
        verbose_name=_('Video playback'),
        help_text=_('Will you play video in your programme?'),
        **TRISTATE_FIELD_PARAMS
    )

    number_of_microphones = models.IntegerField(
        default=1,
        verbose_name=_('Microphones'),
        help_text=_('How many microphones do you require?'),
        choices=[
            (0, '0'),
            (1, '1'),
            (2, '2'),
            (3, '3'),
            (4, '4'),
            (5, '5'),
            (99, _('More than five – Please elaborate on your needs in the "Other tech requirements" field.')),
        ],
    )

    computer = models.CharField(
        default='con',
        choices=COMPUTER_CHOICES,
        max_length=max(len(key) for (key, label) in COMPUTER_CHOICES),
        verbose_name=_('Computer use'),
        help_text=_(
            'What kind of a computer do you wish to use? The use of your own computer is only possible if '
            'agreed in advance.'
        ),
    )

    tech_requirements = models.TextField(
        blank=True,
        verbose_name=_('Other tech requirements'),
        help_text=_('Do you have tech requirements that are not covered by the previous questions?')
    )

    room_requirements = models.TextField(
        blank=True,
        verbose_name=_('Room requirements'),
        help_text=_(
            'How large an audience do you expect for your programme? What kind of a room do you wish for your '
            'programme?'
        ),
    )

    requested_time_slot = models.TextField(
        blank=True,
        verbose_name=_('Requested time slot'),
        help_text=_(
            'At what time would you like to hold your programme? Are there other programme that you do not '
            'wish to co-incide with?'
        ),
    )

    video_permission = models.CharField(
        max_length=15,
        choices=VIDEO_PERMISSION_CHOICES,
        default=VIDEO_PERMISSION_CHOICES[0][0],
        verbose_name=_('Recording permission'),
        help_text=_('May your programme be recorded and published in the Internet?'),
    )

    encumbered_content = models.CharField(
        default='no',
        max_length=max(len(key) for (key, label) in ENCUMBERED_CONTENT_CHOICES),
        choices=ENCUMBERED_CONTENT_CHOICES,
        verbose_name=_('Encumbered content'),
        help_text=_(
            'Encumbered content cannot be displayed on our YouTube channel. Encumbered content will be edited '
            'out of video recordings.'
        ),
    )

    photography = models.CharField(
        default='okay',
        max_length=max(len(key) for (key, label) in PHOTOGRAPHY_CHOICES),
        choices=PHOTOGRAPHY_CHOICES,
        verbose_name=_('Photography of your prorgmme'),
        help_text=_(
            'Our official photographers will try to cover all programmes whose hosts request their programmes '
            'to be photographed.'
        ),
    )

    rerun = models.CharField(
        default='original',
        max_length=max(len(key) for (key, label) in RERUN_CHOICES),
        choices=RERUN_CHOICES,
        verbose_name=_('Is this a re-run?'),
        help_text=_(
            'Have you presented this same programme at another event before the event you are offering '
            'it to now, or do you intend to present it in another event before this one? If you are unsure '
            'about the re-run policy of this event, please consult the programme managers.'
        ),
    )

    notes_from_host = models.TextField(
        blank=True,
        verbose_name=_('Anything else?'),
        help_text=_(
            'If there is anything else you wish to say to the programme manager that is not covered by the '
            'above questions, please enter it here.'
        ),
    )

    state = models.CharField(
        max_length=15,
        choices=STATE_CHOICES,
        default='accepted',
        verbose_name=_('State'),
        help_text=_(
            'The programmes in the state "Published" will be visible to the general public, if the schedule '
            'has already been published.'
        ),
    )

    frozen = models.BooleanField(
        default=False,
        verbose_name=_('Frozen'),
        help_text=_(
            'When a programme is frozen, its details can no longer be edited by the programme host. The '
            'programme manager may continue to edit these, however.'
        ),
    )

    start_time = models.DateTimeField(blank=True, null=True, verbose_name=START_TIME_LABEL)

    # denormalized
    end_time = models.DateTimeField(blank=True, null=True, verbose_name=_('Ending time'))

    length = models.IntegerField(
        blank=True,
        null=True,
        verbose_name=_('Length (minutes)'),
        help_text=_(
            'In order to be displayed in the schedule, the programme must have a start time and a length and '
            'must be assigned into a room.'
        ),
    )
    length_from_host = models.CharField(
        max_length=127,
        blank=True,
        null=True,
        verbose_name='Ohjelman pituus',
        help_text=(
            'Huomaathan, että emme voi taata juuri toivomasi pituista ohjelmapaikkaa. Ohjelmavastaava vahvistaa '
            'ohjelmasi pituuden.'
        ),
    )

    # Originally hitpoint2017 rpg form fields
    rpg_system = models.CharField(
        max_length=512,
        blank=True,
        default='',
        verbose_name=_('RPG system'),
        help_text=_('Which rule system is your RPG using?'),
    )
    approximate_length = models.IntegerField(
        blank=True,
        null=True,
        default=240,
        verbose_name=_('approximate length (minutes)'),
        help_text=_('Please give your best guess on how long you expect your game to take.'),
    )
    physical_play = models.CharField(
        max_length=max(len(key) for (key, text) in PHYSICAL_PLAY_CHOICES),
        default='some',
        choices=PHYSICAL_PLAY_CHOICES,
        verbose_name=_('Amount of physical play'),
        help_text=_(
            'In this context, physical play can mean, for example, using your whole body, acting the actions '
            'of your character or moving around in the allocated space.'
        ),
    )
    is_english_ok = models.BooleanField(
        verbose_name=_('English OK'),
        help_text=_(
            'Please tick this box if you are able, prepared and willing to host your programme in English if '
            'necessary.'
        ),
        default=False,
    )
    is_children_friendly = models.BooleanField(
        verbose_name=_('children-friendly'),
        help_text=_(
            'Please tick this box if your game is suitable for younger players. Please give more details, if '
            'necessary, in the last open field.'
        ),
        default=False,
    )
    is_age_restricted = models.BooleanField(
        verbose_name=_('restricted to people of age 18 and over'),
        help_text=_(
            'Please tick this box if your game contains themes that require it to be restricted to players of '
            '18 years and older.'
        ),
        default=False,
    )
    is_beginner_friendly = models.BooleanField(
        verbose_name=_('beginner friendly'),
        help_text=_('Please tick this box if your game can be enjoyed even without any prior role-playing experience.'),
        default=False,
    )
    is_intended_for_experienced_participants = models.BooleanField(
        verbose_name=_('experienced participants preferred'),
        default=False,
    )
    min_players = models.PositiveIntegerField(
        verbose_name=_('minimum number of players'),
        help_text=_('How many players must there at least be for the game to take place?'),
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(99)],
    )
    max_players = models.PositiveIntegerField(
        verbose_name=_('maximum number of players'),
        help_text=_('What is the maximum number of players that can take part in a single run of the game?'),
        default=4,
        validators=[MinValueValidator(1), MaxValueValidator(99)],
    )
    hitpoint2017_preferred_time_slots = models.ManyToManyField('hitpoint2017.TimeSlot',
        verbose_name=_('preferred time slots'),
        help_text=_(
            'When would you like to run your RPG? The time slots are intentionally vague. If you have more '
            'specific needs regarding the time, please explain them in the last open field.'
        ),
    )

    # XXX BAD, there needs to be a better way if this becomes a recurring pattern
    ropecon2018_preferred_time_slots = models.ManyToManyField('ropecon2018.TimeSlot',
        verbose_name=_('preferred time slots'),
        help_text=_(
            'When would you like to run your RPG? The time slots are intentionally vague. If you have more '
            'specific needs regarding the time, please explain them in the last open field.'
        ),
    )

    other_author = models.CharField(
        max_length=1023,
        blank=True,
        default='',
        verbose_name=_('Author (if other than the GM)'),
        help_text=_(
            'If the scenario has been written by someone else than the GM, we require that the author be '
            'disclosed.'
        ),
    )

    # Internal fields
    notes = models.TextField(
        blank=True,
        verbose_name=_('Internal notes'),
        help_text=_(
            'This field is normally only visible to the programme managers. However, should the programme '
            'host request a record of their own personal details, this field will be included in that record.'
        ),
    )
    room = models.ForeignKey(
        'programme.Room',
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        verbose_name=_('Room'),
        related_name='programmes',
    )
    organizers = models.ManyToManyField('core.Person', through='ProgrammeRole', blank=True)
    tags = models.ManyToManyField('programme.Tag', blank=True, verbose_name=_('Tags'))

    video_link = models.CharField(
        max_length=255,
        blank=True,
        default='',
        verbose_name=_('Video link'),
        help_text=_('A link to a recording of the programme in an external video service such as YouTube'),
    )
    signup_link = models.CharField(
        max_length=255,
        blank=True,
        default='',
        verbose_name=_('Signup link'),
        help_text=_(
            'If the programme requires signing up in advance, put a link here and it will be shown '
            'as a button in the schedule.'
        ),
    )

    created_at = models.DateTimeField(auto_now_add=True, null=True, verbose_name=_('Created at'))
    updated_at = models.DateTimeField(auto_now=True, null=True, verbose_name=_('Updated at'))

    @property
    def event(self):
        return self.category.event

    @property
    def programme_roles(self):
        from .programme_role import ProgrammeRole
        return ProgrammeRole.objects.filter(programme=self)

    @property
    def formatted_hosts(self):
        if not hasattr(self, '_formatted_hosts'):
            from .freeform_organizer import FreeformOrganizer

            parts = [f.text for f in FreeformOrganizer.objects.filter(programme=self)]

            public_programme_roles = self.programme_roles.filter(
                role__is_public=True
            ).select_related('person')

            parts.extend(pr.person.display_name for pr in public_programme_roles)

            self._formatted_hosts = ', '.join(parts)

        return self._formatted_hosts

    @property
    def is_blank(self):
        return False

    def __str__(self):
        return self.title

    @property
    def css_classes(self):
        return self.category.style if self.category.style else ''

    @property
    def is_active(self):
        return self.state in PROGRAMME_STATES_ACTIVE

    @property
    def is_rejected(self):
        return self.state == 'rejected'

    @property
    def is_cancelled(self):
        return self.state == 'cancelled'

    @property
    def is_published(self):
        return self.state == 'published'

    @property
    def is_open_for_feedback(self):
        t = now()
        return (
            (self.end_time is not None and t >= self.end_time) or
            (self.event.end_time is not None and t >= self.event.end_time)
        )

    @property
    def show_signup_link(self):
        t = now()
        return self.signup_link and (
            (self.start_time is not None and t <= self.start_time) or
            (self.event.start_time is not None and t <= self.event.start_time)
        )

    @classmethod
    def get_or_create_dummy(cls, title='Dummy program', state='published'):
        from .category import Category
        from .room import Room

        category, unused = Category.get_or_create_dummy()
        room, unused = Room.get_or_create_dummy()

        return cls.objects.get_or_create(
            title=title,
            defaults=dict(
                category=category,
                room=room,
                state=state,
            )
        )

    @property
    def formatted_start_time(self):
        return format_datetime(self.start_time) if self.start_time else ''

    @property
    def formatted_times(self):
        return '{start_time} – {end_time}'.format(
            start_time=format_datetime(self.start_time),
            end_time=format_datetime(self.end_time),
        )

    # for json
    @property
    def category_title(self):
        return self.category.title

    @property
    def room_name(self):
        return self.room.name if self.room is not None else None

    @property
    def is_public(self):
        return self.state == 'published' and self.category is not None and self.category.public

    def as_json(self, format='default'):
        from core.utils import pick_attrs

        if format == 'default':
            return pick_attrs(self,
                'title',
                'description',
                'category_title',
                'formatted_hosts',
                'room_name',
                'length',
                'start_time',
                'is_public',
            )
        elif format == 'desucon':
            return pick_attrs(self,
                'title',
                'description',
                'start_time',
                'end_time',

                language='fi',  # XXX hardcoded
                status=1 if self.is_public else 0,
                kind=self.category.slug,
                kind_display=self.category.title,
                identifier=self.slug or 'p{id}'.format(id=self.id),
                location=self.room.name if self.room else None,
                location_slug=self.room.slug if self.room else None,
                presenter=self.formatted_hosts,
                tags=list(self.tags.values_list('slug', flat=True)),
            )
        else:
            raise NotImplementedError(format)

    @property
    def state_css(self):
        return STATE_CSS[self.state]

    @property
    def signup_extras(self):
        SignupExtra = self.event.programme_event_meta.signup_extra_model

        if SignupExtra.supports_programme:
            return SignupExtra.objects.filter(event=self.event, person__in=self.organizers.all())
        else:
            return SignupExtra.objects.none()

    def save(self, *args, **kwargs):
        if self.start_time and self.length:
            self.end_time = self.start_time + timedelta(minutes=self.length)

        if self.title and not self.slug:
            self.slug = slugify(self.title)

        return super(Programme, self).save(*args, **kwargs)

    def apply_state(self, deleted_programme_roles=[]):
        self.apply_state_sync(deleted_programme_roles)
        self.apply_state_async()

    def apply_state_sync(self, deleted_programme_roles):
        self.apply_state_update_programme_roles()
        self.apply_state_update_signup_extras()
        self.apply_state_create_badges(deleted_programme_roles)

    def apply_state_async(self):
        if 'background_tasks' in settings.INSTALLED_APPS:
            from ..tasks import programme_apply_state_async
            programme_apply_state_async.delay(self.pk)
        else:
            self._apply_state_async()

    def _apply_state_async(self):
        self.apply_state_group_membership()

    def apply_state_update_programme_roles(self):
        self.programme_roles.update(is_active=self.is_active)

    def apply_state_update_signup_extras(self):
        for signup_extra in self.signup_extras:
            signup_extra.apply_state()

    def apply_state_group_membership(self):
        from django.contrib.auth.models import Group
        from core.utils import ensure_user_group_membership
        from .programme_role import ProgrammeRole

        try:
            group = self.event.programme_event_meta.get_group('hosts')
        except Group.DoesNotExist:
            logger.warning('Event %s missing the programme hosts group', self.event)
            return

        for person in self.organizers.all():
            assert person.user

            if ProgrammeRole.objects.filter(
                programme__category__event=self.event,
                programme__state__in=PROGRAMME_STATES_ACTIVE,
                person=person,
            ).exists():
                # active programmist
                groups_to_add = [group]
                groups_to_remove = []
            else:
                # inactive programmist
                groups_to_add = []
                groups_to_remove = [group]

            ensure_user_group_membership(person.user,
                groups_to_add=groups_to_add,
                groups_to_remove=groups_to_remove
            )


    def apply_state_create_badges(self, deleted_programme_roles=[]):
        if 'badges' not in settings.INSTALLED_APPS:
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

        return (
            cls.objects.filter(q)
            .distinct()
            .order_by('category__event__start_time', 'start_time', 'title')
        )

    @classmethod
    def get_future_programmes(cls, person, t=None):
        if t is None:
            t = now()

        return cls._get_in_states(
            person,
            PROGRAMME_STATES_ACTIVE,
            Q(end_time__gt=t) | Q(end_time__isnull=True) & Q(category__event__end_time__gt=t)
        )

    @classmethod
    def get_past_programmes(cls, person, t=None):
        if t is None:
            t = now()

        return cls._get_in_states(
            person,
            PROGRAMME_STATES_ACTIVE,
            Q(end_time__lte=t) | Q(end_time__isnull=True) & Q(category__event__end_time__lte=t)
        )

    @classmethod
    def get_rejected_programmes(cls, person):
        return cls._get_in_states(person, PROGRAMME_STATES_INACTIVE)

    @property
    def host_can_edit(self):
        return (
            self.state in PROGRAMME_STATES_ACTIVE and
            not self.frozen and
            not (self.event.end_time and now() >= self.event.end_time)
        )

    @property
    def host_cannot_edit_explanation(self):
        assert not self.host_can_edit

        if self.state == 'cancelled':
            return _('You have cancelled this programme.')
        elif self.state == 'rejected':
            return _('This programme has been rejected by the programme manager.')
        elif self.frozen:
            return _('This programme has been frozen by the programme manager.')
        elif now() >= self.event.end_time:
            return _('The event has ended and the programme has been archived.')
        else:
            raise NotImplementedError(self.state)

    def get_feedback_url(self, request=None):
        path = url('programme_feedback_view', self.event.slug, self.pk)

        if request:
            return request.build_absolute_uri(path)
        else:
            return path

    @property
    def visible_feedback(self):
        return self.feedback.filter(hidden_at__isnull=True).select_related('author').order_by('-created_at')

    class Meta:
        verbose_name = _('programme')
        verbose_name_plural = _('programmes')
        ordering = ['start_time', 'room']
        index_together = [('category', 'state')]
        # unique_together = [('category', 'slug')]
