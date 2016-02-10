# encoding: utf-8

from collections import defaultdict, namedtuple, OrderedDict
from datetime import date, datetime, timedelta

from django.conf import settings
from django.db import models
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _

import jsonschema

from core.csv_export import CsvExportMixin
from core.models import EventMetaBase
from core.utils import (
    alias_property,
    ensure_user_group_membership,
    full_hours_between,
    get_previous_and_next,
    is_within_period,
    NONUNIQUE_SLUG_FIELD_PARAMS,
    ONE_HOUR,
    pick_attrs,
    SLUG_FIELD_PARAMS,
    slugify,
    time_bool_property,
)

from .constants import (
    SIGNUP_STATE_NAMES,
    NUM_FIRST_CATEGORIES,
    SIGNUP_STATE_CLASSES,
    SIGNUP_STATE_LABEL_CLASSES,
    SIGNUP_STATE_BUTTON_CLASSES,
    SIGNUP_STATE_DESCRIPTIONS,
    SIGNUP_STATE_IMPERATIVES,
    STATE_FLAGS_BY_NAME,
    STATE_NAME_BY_FLAGS,
    STATE_TIME_FIELDS,
    GROUP_VERBOSE_NAMES_BY_SUFFIX,
    SIGNUP_STATE_GROUPS,
)


class Signup(models.Model, CsvExportMixin):
    person = models.ForeignKey('core.Person')
    event = models.ForeignKey('core.Event')

    personnel_classes = models.ManyToManyField('labour.PersonnelClass',
        blank=True,
        verbose_name=u'Henkilöstöluokat',
        help_text=u'Mihin henkilöstöryhmiin tämä henkilö kuuluu? Henkilö saa valituista ryhmistä '
            u'ylimmän mukaisen badgen.',
    )

    job_categories = models.ManyToManyField('labour.JobCategory',
        verbose_name=u'Haettavat tehtävät',
        help_text=u'Valitse kaikki ne tehtävät, joissa olisit valmis työskentelemään '
            u'tapahtumassa. Huomaathan, että sinulle tarjottavia tehtäviä voi rajoittaa se, '
            u'mitä pätevyyksiä olet ilmoittanut sinulla olevan. Esimerkiksi järjestyksenvalvojaksi '
            u'voivat ilmoittautua ainoastaan JV-kortilliset.',
        related_name='signup_set'
    )

    notes = models.TextField(
        blank=True,
        verbose_name=u'Käsittelijän merkinnät',
        help_text=u'Tämä kenttä ei normaalisti näy henkilölle itselleen, mutta jos tämä '
            u'pyytää henkilörekisteriotetta, kentän arvo on siihen sisällytettävä.'
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=u'Luotu')
    updated_at = models.DateTimeField(auto_now=True, verbose_name=u'Päivitetty')

    job_categories_accepted = models.ManyToManyField('labour.JobCategory',
        blank=True,
        related_name='accepted_signup_set',
        verbose_name=u'Hyväksytyt tehtäväalueet',
        help_text=u'Tehtäväalueet, joilla hyväksytty vapaaehtoistyöntekijä tulee työskentelemään. '
            u'Tämän perusteella henkilölle mm. lähetetään oman tehtäväalueensa työvoimaohjeet. '
            u'Harmaalla merkityt tehtäväalueet ovat niitä, joihin hakija ei ole itse hakenut.'
    )

    job_categories_rejected = models.ManyToManyField('labour.JobCategory',
        blank=True,
        related_name='+',
        verbose_name=_('Rejected job categories'),
        help_text=_(u'The workforce manager may use this field to inform other workforce managers that '
            u'this applicant will not be accepted to a certain job category. This field is not visible '
            u'to the applicant, but should they request a record of their own information, this field will '
            u'be included.')
    )

    xxx_interim_shifts = models.TextField(
        blank=True,
        null=True,
        default=u"",
        verbose_name=u"Työvuorot",
        help_text=u"Tämä tekstikenttä on väliaikaisratkaisu, jolla vänkärin työvuorot voidaan "
            u"merkitä Kompassiin ja lähettää vänkärille työvoimaviestissä jo ennen kuin "
            u"lopullinen työvuorotyökalu on käyttökunnossa."
    )

    alternative_signup_form_used = models.ForeignKey('labour.AlternativeSignupForm',
        blank=True,
        null=True,
        verbose_name=u"Ilmoittautumislomake",
        help_text=u"Tämä kenttä ilmaisee, mitä ilmoittautumislomaketta hakemuksen täyttämiseen käytettiin. "
            u"Jos kenttä on tyhjä, käytettiin oletuslomaketta.",
    )

    job_title = models.CharField(
        max_length=63,
        blank=True,
        default=u'',
        verbose_name=u"Tehtävänimike",
        help_text=u"Printataan badgeen ym. Asetetaan automaattisesti hyväksyttyjen tehtäväalueiden perusteella, mikäli kenttä jätetään tyhjäksi.",
    )

    is_active = models.BooleanField(verbose_name=u'Aktiivinen', default=True)

    time_accepted = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=u'Hyväksytty',
    )

    time_confirmation_requested = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=u'Vahvistusta vaadittu',
    )

    time_finished = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=u'Vuorot valmiit',
    )

    time_complained = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=u'Vuoroista reklamoitu',
    )

    time_cancelled = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=u'Peruutettu',
    )

    time_rejected = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=u'Hylätty',
    )

    time_arrived = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=u'Saapunut tapahtumaan',
    )

    time_work_accepted = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=u'Työpanos hyväksytty',
    )

    time_reprimanded = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=u'Työpanoksesta esitetty moite',
    )

    is_accepted = time_bool_property('time_accepted')
    is_confirmation_requested = time_bool_property('time_confirmation_requested')
    is_finished = time_bool_property('time_finished')
    is_complained = time_bool_property('time_complained')
    is_cancelled = time_bool_property('time_cancelled')
    is_rejected = time_bool_property('time_rejected')
    is_arrived = time_bool_property('time_arrived')
    is_work_accepted = time_bool_property('time_work_accepted')
    is_workaccepted = alias_property('is_work_accepted') # for automagic groupiness
    is_reprimanded = time_bool_property('time_reprimanded')

    is_new = property(lambda self: self.state == 'new')
    is_applicants = alias_property('is_active') # group is called applicants for historical purposes
    is_confirmation = alias_property('is_confirmation_requested')
    is_processed = property(lambda self: self.state != 'new')

    class Meta:
        verbose_name = _(u'signup')
        verbose_name_plural = _(u'signups')

    def __unicode__(self):
        p = self.person.full_name if self.person else 'None'
        e = self.event.name if self.event else 'None'

        return u'{p} / {e}'.format(**locals())

    @property
    def signup_extra_model(self):
        return self.event.labour_event_meta.signup_extra_model

    @property
    def signup_extra(self):
        if not hasattr(self, '_signup_extra'):
            SignupExtra = self.signup_extra_model
            try:
                self._signup_extra = SignupExtra.objects.get(signup=self)
            except SignupExtra.DoesNotExist:
                self._signup_extra = SignupExtra(signup=self)

        return self._signup_extra

    def get_first_categories(self):
        return self.job_categories.all()[:NUM_FIRST_CATEGORIES]

    @property
    def is_more_categories(self):
        return self.job_categories.count() > NUM_FIRST_CATEGORIES

    def get_redacted_category_names(self):
        return u', '.join(cat.name for cat in self.job_categories.all()[NUM_FIRST_CATEGORIES:])

    @property
    def job_categories_label(self):
        if self.state == 'new':
            return u'Haetut tehtävät'
        else:
            return u'Hyväksytyt tehtävät'

    @property
    def job_category_accepted_labels(self):
        state = self.state
        label_class = SIGNUP_STATE_LABEL_CLASSES[state]

        if state == 'new':
            label_texts = [cat.name for cat in self.get_first_categories()]
            labels = [(label_class, label_text, None) for label_text in label_texts]

            if self.is_more_categories:
                labels.append((label_class, u'...', self.get_redacted_category_names()))

        elif state == 'cancelled':
            labels = [(label_class, u'Peruutettu', None)]

        elif state == 'rejected':
            labels = [(label_class, u'Hylätty', None)]

        elif state == 'beyond_logic':
            labels = [(label_class, u'Perätilassa', None)]

        elif self.is_accepted:
            label_texts = [cat.name for cat in self.job_categories_accepted.all()]
            labels = [(label_class, label_text, None) for label_text in label_texts]

        else:
            from warnings import warn
            warn(u'Unknown state: {state}'.format(self=self))
            labels = []

        return labels

    @property
    def personnel_class_labels(self):
        state = self.state
        label_texts = [pc.name for pc in self.personnel_classes.all()]
        return [('label-default', label_text, None) for label_text in label_texts]

    @property
    def some_job_title(self):
        """
        Tries to figure a job title for this worker using the following methods in this order

        1. A manually set job title
        2. The title of the job category the worker is accepted into
        3. A generic job title
        """

        if self.job_title:
            return self.job_title
        elif self.job_categories_accepted.exists():
            return self.job_categories_accepted.first().name
        else:
            return u'Työvoima'

    @property
    def granted_privileges(self):
        if 'access' not in settings.INSTALLED_APPS:
            return []

        from access.models import GrantedPrivilege

        return GrantedPrivilege.objects.filter(
            person=self.person,
            privilege__group_privileges__group__in=self.person.user.groups.all(),
            privilege__group_privileges__event=self.event,
        )

    @property
    def potential_privileges(self):
        if 'access' not in settings.INSTALLED_APPS:
            return []

        from access.models import Privilege

        return Privilege.get_potential_privileges(person=self.person, group_privileges__event=self.event)

    @classmethod
    def get_or_create_dummy(cls, accepted=False):
        from core.models import Person, Event
        from .job_category import JobCategory

        person, unused = Person.get_or_create_dummy()
        event, unused = Event.get_or_create_dummy()
        job_category, unused = JobCategory.get_or_create_dummy()

        signup, created = Signup.objects.get_or_create(person=person, event=event)
        extra = signup.signup_extra
        signup.job_categories = [job_category]
        extra.save()

        if accepted:
            signup.job_categories_accepted = signup.job_categories.all()
            signup.personnel_classes.add(signup.job_categories.first().personnel_classes.first())
            signup.state = 'accepted'
            signup.save()
            signup.apply_state()

        return signup, created

    @classmethod
    def get_state_query_params(cls, state):
        flag_values = STATE_FLAGS_BY_NAME[state]
        assert len(STATE_TIME_FIELDS) == len(flag_values)

        query_params = []

        for time_field_name, flag_value in zip(STATE_TIME_FIELDS, flag_values):
            time_field_preposition = '{}__isnull'.format(time_field_name)
            query_params.append((time_field_preposition, not flag_value))

        # First state flag is not a time bool field, but an actual bona fide boolean field.
        # Also "is null" semantics mean that flag values are flipped, so we need to backflip it.
        query_params[0] = ('is_active', not query_params[0][1])

        return OrderedDict(query_params)

    @classmethod
    def mass_reject(cls, signups):
        return cls._mass_state_change('new', 'rejected', signups)

    @classmethod
    def mass_request_confirmation(cls, signups):
        return cls._mass_state_change('accepted', 'confirmation', signups)

    @classmethod
    def _mass_state_change(cls, old_state, new_state, signups):
        signups = signups.filter(**Signup.get_state_query_params(old_state))

        for signup in signups:
            signup.state = new_state
            signup.save()
            signup.apply_state()

        return signups

    def apply_state(self):
        self.apply_state_sync()

        if 'background_tasks' in settings.INSTALLED_APPS:
            from ..tasks import signup_apply_state
            signup_apply_state.delay(self.pk)
        else:
            self._apply_state()

    def apply_state_sync(self):
        self.apply_state_ensure_job_categories_accepted_is_set()
        self.apply_state_ensure_personnel_class_is_set()
        self.apply_state_create_badges()
        self.apply_state_email_aliases()

    def _apply_state(self):
        self.apply_state_group_membership()
        self.apply_state_send_messages()

    def apply_state_group_membership(self):
        from .job_category import JobCategory

        groups_to_add = set()
        groups_to_remove = set()

        for group_suffix in SIGNUP_STATE_GROUPS:
            should_belong_to_group = getattr(self, 'is_{group_suffix}'.format(group_suffix=group_suffix))
            group = self.event.labour_event_meta.get_group(group_suffix)

            if should_belong_to_group:
                groups_to_add.add(group)
            else:
                groups_to_remove.add(group)

        for job_category in JobCategory.objects.filter(event=self.event):
            should_belong_to_group = self.job_categories_accepted.filter(pk=job_category.pk).exists()
            group = self.event.labour_event_meta.get_group(job_category.slug)

            if should_belong_to_group:
                groups_to_add.add(group)
            else:
                groups_to_remove.add(group)

        ensure_user_group_membership(self.person.user, groups_to_add, groups_to_remove)

    def apply_state_email_aliases(self):
        if 'access' not in settings.INSTALLED_APPS:
            return

        from access.models import GroupEmailAliasGrant
        GroupEmailAliasGrant.ensure_aliases(self.person)

    def apply_state_send_messages(self, resend=False):
        if 'mailings' not in settings.INSTALLED_APPS:
            return

        from mailings.models import Message
        Message.send_messages(self.event, 'labour', self.person)

    def apply_state_ensure_job_categories_accepted_is_set(self):
        if self.is_accepted and not self.job_categories_accepted.exists() and self.job_categories.count() == 1:
            self.job_categories_accepted.add(self.job_categories.get())

    def apply_state_ensure_personnel_class_is_set(self):
        for app_label in self.job_categories_accepted.values_list('app_label', flat=True).distinct():
            if self.personnel_classes.filter(app_label=app_label).exists():
                continue

            any_jca = self.job_categories_accepted.filter(app_label=app_label).first()
            personnel_class = any_jca.personnel_classes.first()
            self.personnel_classes.add(personnel_class)

    def apply_state_create_badges(self):
        if 'badges' not in settings.INSTALLED_APPS:
            return

        if self.event.badges_event_meta is None:
            return

        from badges.models import Badge

        Badge.ensure(event=self.event, person=self.person)

    def get_previous_and_next_signup(self):
        queryset = self.event.signup_set.order_by('person__surname', 'person__first_name', 'id').all()
        return get_previous_and_next(queryset, self)

    @property
    def _state_flags(self):
        # The Grand Order is defined here.
        return (
            self.is_active,
            self.is_accepted,
            self.is_confirmation_requested,
            self.is_finished,
            self.is_complained,
            self.is_arrived,
            self.is_work_accepted,
            self.is_reprimanded,
            self.is_rejected,
            self.is_cancelled,
        )

    @_state_flags.setter
    def _state_flags(self, flags):
        # These need to be in the Grand Order.
        (
            self.is_active,
            self.is_accepted,
            self.is_confirmation_requested,
            self.is_finished,
            self.is_complained,
            self.is_arrived,
            self.is_work_accepted,
            self.is_reprimanded,
            self.is_rejected,
            self.is_cancelled,
        ) = flags

    @property
    def state(self):
        return STATE_NAME_BY_FLAGS[self._state_flags]

    @state.setter
    def state(self, new_state):
        self._state_flags = STATE_FLAGS_BY_NAME[new_state]

    @property
    def next_states(self):
        cur_state = self.state

        states = []

        if cur_state == 'new':
            states.extend(('accepted', 'rejected', 'cancelled'))
        elif cur_state == 'accepted':
            states.extend(('finished', 'confirmation', 'cancelled'))
        elif cur_state == 'confirmation':
            states.extend(('accepted', 'cancelled'))
        elif cur_state == 'finished':
            states.extend(('arrived', 'complained', 'no_show', 'relieved'))
        elif cur_state == 'complained':
            states.extend(('finished', 'relieved'))
        elif cur_state == 'arrived':
            states.extend(('honr_discharged', 'dish_discharged', 'relieved'))
        elif cur_state == 'beyond_logic':
            states.extend(('new', 'accepted', 'finished', 'complained', 'rejected', 'cancelled', 'arrived', 'honr_discharged', 'no_show'))

        if cur_state != 'beyond_logic':
            states.append('beyond_logic')

        return states

    @property
    def next_states_buttons(self):
        return [(
            state_name,
            SIGNUP_STATE_BUTTON_CLASSES[state_name],
            SIGNUP_STATE_IMPERATIVES[state_name],
        ) for state_name in self.next_states]

    @property
    def formatted_state(self):
        return dict(SIGNUP_STATE_NAMES).get(self.state, '')

    @property
    def state_label_class(self):
        return SIGNUP_STATE_LABEL_CLASSES[self.state]

    @property
    def state_description(self):
        return SIGNUP_STATE_DESCRIPTIONS.get(self.state, '')

    @property
    def state_times(self):
        return [
            (
                self._meta.get_field_by_name(field_name)[0].verbose_name,
                getattr(self, field_name, None),
            )
            for field_name in STATE_TIME_FIELDS
            if getattr(self, field_name, None)
        ]

    @property
    def person_messages(self):
        if 'mailings' in settings.INSTALLED_APPS:
            if getattr(self, '_person_messages', None) is None:
                self._person_messages = self.person.personmessage_set.filter(
                    message__recipient__event=self.event,
                    message__recipient__app_label='labour',
                ).order_by('-created_at')

            return self._person_messages
        else:
            return []

    @property
    def have_person_messages(self):
        if 'mailings' in settings.INSTALLED_APPS:
            return self.person_messages.exists()
        else:
            return False

    @property
    def applicant_has_actions(self):
        return any([
            self.applicant_can_edit,
            self.applicant_can_confirm,
            self.applicant_can_cancel,
        ])

    @property
    def applicant_can_edit(self):
        return self.state == 'new' and self.is_registration_open

    @property
    def is_registration_open(self):
        if self.alternative_signup_form_used is not None:
            return self.alternative_signup_form_used.is_active
        else:
            return self.event.labour_event_meta.is_registration_open

    @property
    def applicant_can_confirm(self):
        return self.state == 'confirmation'

    def confirm(self):
        assert self.state == 'confirmation'

        self.state = 'accepted'
        self.save()
        self.apply_state()

    @property
    def applicant_can_cancel(self):
        return self.is_active and not self.is_cancelled and not self.is_rejected and \
            not self.is_arrived

    @property
    def formatted_job_categories_accepted(self):
        from .job_category import format_job_categories
        return format_job_categories(self.job_categories_accepted.all())

    @property
    def formatted_job_categories(self):
        from .job_category import format_job_categories
        return format_job_categories(self.job_categories.all())

    @property
    def formatted_shifts(self):
        return self.xxx_interim_shifts if self.xxx_interim_shifts is not None else u""

    # for admin
    @property
    def full_name(self):
        return self.person.full_name

    @property
    def info_links(self):
        from .info_link import InfoLink

        return InfoLink.objects.filter(
            event=self.event,
            group__user=self.person.user,
        )

    @classmethod
    def get_csv_fields(cls, event):
        if getattr(event, '_signup_csv_fields', None) is None:
            from core.models import Person

            event._signup_csv_fields = []

            related_models = [Person, Signup]

            SignupExtra = event.labour_event_meta.signup_extra_model
            if SignupExtra is not None:
                related_models.append(SignupExtra)

            # XXX HACK jv-kortin numero
            if 'labour_common_qualifications' in settings.INSTALLED_APPS:
                from labour_common_qualifications.models import JVKortti
                related_models.append(JVKortti)

            for model in related_models:
                for field in model._meta.fields:
                    if not isinstance(field, models.ForeignKey):
                        event._signup_csv_fields.append((model, field))

                for field, unused in model._meta.get_m2m_with_model():
                    event._signup_csv_fields.append((model, field))

        return event._signup_csv_fields

    def get_csv_related(self):
        from core.models import Person
        related = {Person: self.person}

        signup_extra_model = self.signup_extra_model
        if signup_extra_model:
            related[signup_extra_model] = self.signup_extra

        # XXX HACK jv-kortin numero
        if 'labour_common_qualifications' in settings.INSTALLED_APPS:
            from labour_common_qualifications.models import JVKortti
            try:
                jv_kortti = JVKortti.objects.get(personqualification__person__signup=self)
                related[JVKortti] = jv_kortti
            except JVKortti.DoesNotExist:
                related[JVKortti] = None

        return related
