# encoding: utf-8

from datetime import date, datetime, timedelta

from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.timezone import now

from core.models import EventMetaBase
from core.utils import (
    SLUG_FIELD_PARAMS,
    ensure_user_is_member_of_group,
    ensure_user_is_not_member_of_group,
)


GROUP_VERBOSE_NAMES_BY_SUFFIX = dict(
    admins=u'Työvoimavastaavat',
    applicants=u'Hakijat',
    accepted=u'Hyväksytyt',
    finished=u'Työvuorotetut',
    rejected=u'Hylätyt',
)


class LabourEventMeta(EventMetaBase):
    signup_extra_content_type = models.ForeignKey('contenttypes.ContentType')

    registration_opens = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=u'työvoimahaku alkaa'
    )

    registration_closes = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=u'työvoimahaku päättyy'
    )

    work_begins = models.DateTimeField(verbose_name=u'Ensimmäiset työvuorot alkavat')
    work_ends = models.DateTimeField(verbose_name=u'Viimeiset työvuorot päättyvät')

    monitor_email = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=u'tarkkailusähköposti',
        help_text=u'Kaikki työvoimajärjestelmän lähettämät sähköpostiviestit lähetetään myös '
            u'tähän osoitteeseen.',
    )

    contact_email = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=u'yhteysosoite',
        help_text=u'Kaikki työvoimajärjestelmän lähettämät sähköpostiviestit lähetetään tästä '
            u'osoitteesta, ja tämä osoite näytetään työvoimalle yhteysosoitteena. Muoto: Selite &lt;osoite@esimerkki.fi&gt;.',
    )

    applicants_group = models.ForeignKey('auth.Group',
        verbose_name=u'Hakijoiden ryhmä',
        help_text=u'Järjestelmä lisää kaikki työvoimaan hakeneet automaattisesti tähän '
            u'käyttäjäryhmään pääsynvalvontaa varten.',
        related_name='+',
    )

    accepted_group = models.ForeignKey('auth.Group',
        verbose_name=u'Työvoimaan hyväksyttyjen ryhmä',
        help_text=u'Järjestelmä lisää kaikki työvoimaan hyväksytyt automaattisesti tähän '
            u'käyttäjäryhmään pääsynvalvontaa varten.',
        related_name='+',
    )

    finished_group = models.ForeignKey('auth.Group',
        verbose_name=u'Vuorotettujen vänkärien ryhmä',
        help_text=u'Järjestelmä lisää tähän ryhmään automaattisesti kaikki ne hyväksytyt '
            u'vänkärit, joille on tehty työvuorot valmiiksi.',
        related_name='+',
    )

    rejected_group = models.ForeignKey('auth.Group',
        verbose_name=u'Hylättyjen vänkäriehdokkaiden ryhmä',
        help_text=u'Järjestelmä lisää tähän ryhmään automaattisesti kaikki ne vänkärihakijat, '
            u'joiden hakemukset työvoimavastaava on hylännyt.',
        related_name='+',
    )

    class Meta:
        verbose_name = u'tapahtuman työvoimatiedot'
        verbose_name_plural = u'tapahtuman työvoimatiedot'

    def __unicode__(self):
        return self.event.name if self.event else 'None'

    @property
    def signup_extra_model(self):
        return self.signup_extra_content_type.model_class()

    @classmethod
    def events_registration_open(cls):
        from core.models import Event
        t = now()
        return Event.objects.filter(
            laboureventmeta__registration_opens__isnull=False,
            laboureventmeta__registration_opens__lte=t,
        ).exclude(
            laboureventmeta__registration_closes__isnull=False,
            laboureventmeta__registration_closes__lte=t,
        )

    @classmethod
    def get_or_create_dummy(cls):
        from core.models import Event
        from django.contrib.contenttypes.models import ContentType

        event, unused = Event.get_or_create_dummy()
        content_type = ContentType.objects.get_for_model(EmptySignupExtra)
        admin_group, unused = cls.get_or_create_group(event, 'admins')
        accepted_group, unused = cls.get_or_create_group(event, 'accepted')
        applicants_group, unused = cls.get_or_create_group(event, 'applicants')
        finished_group, unused = cls.get_or_create_group(event, 'finished')
        rejected_group, unused = cls.get_or_create_group(event, 'rejected')

        t = now()

        return cls.objects.get_or_create(
            event=event,
            defaults=dict(
                admin_group=admin_group,
                accepted_group=accepted_group,
                applicants_group=applicants_group,
                finished_group=finished_group,
                rejected_group=rejected_group,
                signup_extra_content_type=content_type,
                registration_opens=t - timedelta(days=60),
                registration_closes=t + timedelta(days=60),
                work_begins=event.start_time - timedelta(days=1),
                work_ends=event.end_time + timedelta(days=1),
                contact_email='dummy@example.com',
                monitor_email='dummy@example.com',
            )
        )

    @classmethod
    def get_or_create_group(cls, event, suffix):
        group, created = super(LabourEventMeta, cls).get_or_create_group(event, suffix)

        if 'mailings' in settings.INSTALLED_APPS:
            from mailings.models import RecipientGroup

            RecipientGroup.objects.get_or_create(
                event=event,
                app_label='labour',
                group=group,
                defaults=dict(
                    verbose_name=GROUP_VERBOSE_NAMES_BY_SUFFIX.get(suffix, suffix),
                ),
            )

        return group, created

    @property
    def is_registration_open(self):
        t = now()
        return self.registration_opens and self.registration_opens <= t and \
            not (self.registration_closes and self.registration_closes <= t)

    def is_person_signed_up(self, person):
        return Signup.objects.filter(person=person, event=self.event).exists()

    def get_signup_for_person(self, person):
        try:
            return Signup.objects.get(person=person, event=self.event)
        except Signup.DoesNotExist:
            return Signup(person=person, event=self.event)

    def is_user_admin(self, user):
        if not user.is_authenticated():
            return False

        if user.is_superuser:
            return True

        return user.groups.filter(pk=self.admin_group.pk).exists()

    @property
    def work_hours(self):
        from programme.utils import full_hours_between
        return full_hours_between(self.work_begins, self.work_ends)


class Qualification(models.Model):
    slug = models.CharField(**SLUG_FIELD_PARAMS)

    name = models.CharField(max_length=63, verbose_name=u'pätevyyden nimi')
    description = models.TextField(blank=True, verbose_name=u'kuvaus')

    qualification_extra_content_type = models.ForeignKey('contenttypes.ContentType', null=True, blank=True)

    class Meta:
        verbose_name = u'pätevyys'
        verbose_name_plural = u'pätevyydet'

    def __unicode__(self):
        return self.name

    @property
    def qualification_extra_model(self):
        if self.qualification_extra_content_type:
            return self.qualification_extra_content_type.model_class()
        else:
            return None

    @classmethod
    def create_dummy(cls):
        return cls.objects.create(
            name='Dummy qualification'
        )

    @classmethod
    def get_or_create_dummies(cls):
        qual1, unused = Qualification.objects.get_or_create(slug='dummy1', defaults=dict(
            name='Dummy qualification 1'
        ))
        qual2, unused = Qualification.objects.get_or_create(slug='dummy2', defaults=dict(
            name='Dummy qualification 2'
        ))
        return [qual1, qual2]


class PersonQualification(models.Model):
    person = models.ForeignKey('core.Person', verbose_name=u'henkilö')
    qualification = models.ForeignKey(Qualification, verbose_name=u'pätevyys')

    class Meta:
        verbose_name = u'pätevyyden haltija'
        verbose_name_plural=u'pätevyyden haltijat'

    def __unicode__(self):
        return self.qualification.name if self.qualification else 'None'

    @property
    def qualification_extra(self):
        if not self.qualification:
            return None

        QualificationExtra = self.qualification.qualification_extra_model
        if not QualificationExtra:
            return None

        try:
            return QualificationExtra.objects.get(personqualification=self)
        except QualificationExtra.DoesNotExist:
            return QualificationExtra(personqualification=self)


class QualificationExtraBase(models.Model):
    personqualification = models.OneToOneField(PersonQualification,
        related_name="+",
        primary_key=True)

    @classmethod
    def get_form_class(cls):
        raise NotImplemented(
            'Remember to override get_form_class in your QualificationExtra model'
        )

    class Meta:
        abstract = True


def format_job_categories(job_categories):
    return u"\n".join(u'* {jc.name}'.format(jc=jc) for jc in job_categories)


class JobCategory(models.Model):
    event = models.ForeignKey('core.Event', verbose_name=u'tapahtuma')

    name = models.CharField(max_length=63, verbose_name=u'tehtäväalueen nimi')

    description = models.TextField(
        verbose_name=u'tehtäväalueen kuvaus',
        help_text=u'Kuvaus näkyy hakijoille hakulomakkeella. Kerro ainakin, mikäli tehtävään tarvitaan erityisiä tietoja tai taitoja.',
        blank=True
    )

    public = models.BooleanField(
        default=True,
        verbose_name=u'avoimessa haussa',
        help_text=u'Tehtäviin, jotka eivät ole avoimessa haussa, voi hakea vain työvoimavastaavan lähettämällä hakulinkillä.'
    )

    required_qualifications = models.ManyToManyField(Qualification,
        blank=True,
        verbose_name=u'vaaditut pätevyydet'
    )

    def is_person_qualified(self, person):
        if not self.required_qualifications.exists():
            return True

        else:
            quals = [pq.qualification for pq in person.personqualification_set.all()]
            return all(qual in quals for qual in self.required_qualifications.all())

    class Meta:
        verbose_name = u'tehtäväalue'
        verbose_name_plural=u'tehtäväalueet'

    def __unicode__(self):
        return self.name

    @classmethod
    def get_or_create_dummies(cls):
        from core.models import Event
        event, unused = Event.get_or_create_dummy()
        jc1, unused = cls.objects.get_or_create(event=event, name='Dummy 1')
        jc2, unused = cls.objects.get_or_create(event=event, name='Dummy 2')

        return [jc1, jc2]


class WorkPeriod(models.Model):
    event = models.ForeignKey('core.Event', verbose_name=u'Tapahtuma')

    description = models.CharField(
        max_length=63,
        verbose_name=u'Kuvaus'
    )

    start_time = models.DateTimeField(verbose_name=u'Alkuaika')
    end_time = models.DateTimeField(verbose_name=u'Loppuaika')

    class Meta:
        verbose_name = u'työvuorotoive'
        verbose_name_plural=u'työvuorotoiveet'

    def __unicode__(self):
        return self.description


ONE_HOUR = timedelta(hours=1)


class Job(models.Model):
    job_category = models.ForeignKey(JobCategory, verbose_name=u'tehtäväalue')
    title = models.CharField(max_length=63, verbose_name=u'tehtävän nimi')

    class Meta:
        verbose_name = u'tehtävä'
        verbose_name_plural = u'tehtävät'

    def __unicode__(self):
        return self.title

    @property
    def expanded_requirements(self):
        requirements = []

        for hour in self.job_category.event.labour_event_meta.work_hours:
            try:
                job_requirement = self.jobrequirement_set.get(
                    start_time__lte=hour,
                    end_time__gt=hour,
                )
                count = job_requirement.count
            except JobRequirement.DoesNotExist:
                count = 0

            requirements.append(JobRequirement(
                job=self,
                start_time=hour,
                end_time=hour + ONE_HOUR,
                count=count
            ))

        return requirements


class JobRequirement(models.Model):
    job = models.ForeignKey(Job, verbose_name=u'tehtävä')

    count = models.IntegerField(
        verbose_name=u'vaadittu henkilömäärä',
        validators=[MinValueValidator(0)],
        default=0
    )

    start_time = models.DateTimeField(verbose_name=u'vaatimuksen alkuaika')
    end_time = models.DateTimeField(verbose_name=u'vaatimuksen päättymisaika')

    class Meta:
        verbose_name = u'henkilöstövaatimus'
        verbose_name_plural = u'henkilöstövaatimukset'


NUM_FIRST_CATEGORIES = 5
SIGNUP_STATE_CHOICES = [
    (u'new', u'Uusi'),
    (u'accepted', u'Hyväksytty, odottaa vuoroja'),
    (u'finished', u'Hyväksytty, vuorot lähetetty'),
    (u'complained', u'Hyväksytty, vuorot lähetetty, vuoroista reklamoitu'),

    (u'rejected', u'Hylätty (työvoimavastaava ei hyväksynyt töihin)'),
    (u'cancelled', u'Peruutettu (hakijan itsensä peruma)'),

    (u'arrived', u'Saapunut tapahtumaan'),

    (u'honr_discharged', u'Työpanos suoritettu hyväksytysti'),
    (u'dish_discharged', u'Erotettu tehtävästään'),
    (u'no_show', u'Jätti saapumatta paikalle'),
    (u'relieved', u'Vapautettu tehtävästään'),

    (u'beyond_logic', u'Perätilassa (irrotettu kaikesta automaattisesta käsittelystä)'),
]

ACCEPTED_STATES = ['accepted', 'finished', 'complained', 'arrived']
FINISHED_STATES = ['finished', 'complained', 'arrived']
ACTIVE_STATES = ACCEPTED_STATES + ['new']
TERMINAL_STATES = ['rejected', 'cancelled', 'dish_discharged', 'no_show', 'relieved']
PROCESSED_STATES = ACCEPTED_STATES + TERMINAL_STATES
PREEVENT_STATES = ['new', 'accepted', 'finished', 'complained']
SIGNUP_STATE_LABEL_CLASSES = dict(
    new=u'label-default',
    accepted=u'label-info',
    finished=u'label-success',
    complained=u'label-warning',
    rejected=u'label-danger',
    cancelled=u'label-danger',
    arrived=u'label-success',
    honr_discharged=u'label-success',
    dish_discharged=u'label-danger',
    no_show=u'label-danger',
    relieved=u'label-danger',
    beyond_logic=u'label-danger',
)
SIGNUP_STATE_DESCRIPTIONS = dict(
    new=u'Hakemuksesi on vastaanotettu, ja työvoimavastaavat käsittelevät sen lähiaikoina. Saat tiedon hakemuksesi hyväksymisestä tai hylkäämisestä sähköpostitse.',
    accepted=u'Työvoimavastaavat ovat alustavasti hyväksyneet sinut vapaaehtoistyöhön tähän tapahtumaan, mutta sinulle ei ole vielä määritelty työvuoroja. Saat tiedon työvuoroistasi myöhemmin sähköpostitse.',
)

class Signup(models.Model):
    person = models.ForeignKey('core.Person')
    event = models.ForeignKey('core.Event')

    state = models.CharField(
        max_length=15,
        verbose_name=u'Hakemuksen tila',
        choices=SIGNUP_STATE_CHOICES,
        help_text=u'Hakemuksen tilan muuttaminen lähettää automaattisesti henkilölle kyseiseen '
            u'tilasiirtymään liittyvät sähköpostiviestit.',
        default='new',
    )

    job_categories = models.ManyToManyField(JobCategory,
        verbose_name=u'Haettavat tehtävät',
        help_text=u'Valitse kaikki ne tehtävät, joissa olisit valmis työskentelemään '
            u'tapahtumassa. Huomaathan, että sinulle tarjottavia tehtäviä voi rajoittaa se, '
            u'mitä pätevyyksiä olet ilmoittanut sinulla olevan. Esimerkiksi järjestyksenvalvojaksi '
            u'voivat ilmoittautua ainoastaan JV-kortilliset.',
        related_name='signup_set'
    )

    work_periods = models.ManyToManyField(WorkPeriod,
        verbose_name=u'Työvuorotoiveet',
        help_text=u'Valitse kaikki ne ajanjaksot, joina voit työskennellä tapahtumassa. '
            u'Tämä ei ole lopullinen työvuorosi, vaan työvoimatiimi pyrkii sijoittamaan '
            u'työvuorosi näille ajoille.',
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

    job_categories_accepted = models.ManyToManyField(JobCategory,
        blank=True,
        null=True,
        related_name='accepted_signup_set',
        verbose_name=u'Tehtäväalueet',
        help_text=u'Tehtäväalueet, joilla hyväksytty vapaaehtoistyöntekijä tulee työskentelemään. '
            u'Tämän perusteella henkilölle mm. lähetetään oman tehtäväalueensa työvoimaohjeet. '
            u'Harmaalla merkityt tehtäväalueet ovat niitä, joihin hakija ei ole itse hakenut.'
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

    class Meta:
        verbose_name = u'ilmoittautuminen'
        verbose_name_plural=u'ilmoittautumiset'

    def __unicode__(self):
        p = self.person.full_name if self.person else 'None'
        e = self.event.name if self.event else 'None'

        return u'{p} / {e}'.format(**locals())

    @property
    def signup_extra(self):
        if not hasattr(self, '_signup_extra'):
            SignupExtra = self.event.labour_event_meta.signup_extra_model
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
        label_class = SIGNUP_STATE_LABEL_CLASSES[self.state]

        if self.state == 'new':
            label_texts = [cat.name for cat in self.get_first_categories()]
            labels = [(label_class, label_text, None) for label_text in label_texts]

            if self.is_more_categories:
                labels.append((label_class, u'...', self.get_redacted_category_names()))

        elif self.state in ACCEPTED_STATES:
            label_texts = [cat.name for cat in self.job_categories_accepted.all()]
            labels = [(label_class, label_text, None) for label_text in label_texts]

        elif self.state == 'cancelled':
            labels = [(label_class, u'Peruutettu', None)]

        elif self.state == 'rejected':
            labels = [(label_class, u'Hylätty', None)]

        elif self.state == 'beyond_logic':
            labels = [(label_class, u'Perätilassa', None)]

        else:
            from warnings import warn
            warn(u'Unknown state: {self.state}'.format(self=self))
            labels = []

        return labels

    @property
    def is_accepted(self):
        return self.state in ACCEPTED_STATES

    @property
    def is_active(self):
        return self.state in ACTIVE_STATES

    @classmethod
    def get_or_create_dummy(cls):
        from core.models import Person, Event

        person, unused = Person.get_or_create_dummy()
        event, unused = Event.get_or_create_dummy()

        signup, created = Signup.objects.get_or_create(person=person, event=event)
        extra = signup.signup_extra
        extra.save()

        return signup, created

    def state_change_from(self, old_state):
        new_state = self.state

        if new_state == old_state:
            return

        meta = self.event.labour_event_meta

        ensure_user_is_member_of_group(self.person, meta.applicants_group, new_state in ACTIVE_STATES)
        ensure_user_is_member_of_group(self.person, meta.accepted_group,   new_state in ACCEPTED_STATES)
        ensure_user_is_member_of_group(self.person, meta.finished_group,   new_state in FINISHED_STATES)
        ensure_user_is_member_of_group(self.person, meta.rejected_group,   new_state == 'rejected')

        self.send_messages()

    def send_messages(self, resend=False):
        if 'mailings' not in settings.INSTALLED_APPS:
            return

        from mailings.models import Message
        Message.send_messages(self.event, 'labour', self.person)

    def get_previous_and_next_signup(self):
        if not self.pk:
            return None, None

        # TODO inefficient, done using a list
        signups = list(self.event.signup_set.order_by('person__surname', 'person__first_name', 'id').all())

        previous_signup = None
        current_signup = None

        for next_signup in signups + [None]:
            if current_signup and current_signup.pk == self.pk:
                return previous_signup, next_signup

            previous_signup = current_signup
            current_signup = next_signup

        return None, None

    @property
    def formatted_state(self):
        return dict(SIGNUP_STATE_CHOICES).get(self.state, '')

    @property
    def state_label_class(self):
        return SIGNUP_STATE_LABEL_CLASSES[self.state]

    @property
    def state_description(self):
        return SIGNUP_STATE_DESCRIPTIONS.get(self.state, '')

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
            self.applicant_can_cancel,
        ])

    @property
    def applicant_can_edit(self):
        return self.state == 'new'

    @property
    def applicant_can_cancel(self):
        return self.state in PREEVENT_STATES

    @property
    def formatted_job_categories_accepted(self):
        return format_job_categories(self.job_categories_accepted.all())

    @property
    def formatted_job_categories(self):
        return format_job_categories(self.job_categories.all())

    @property
    def formatted_shifts(self):
        return self.xxx_interim_shifts if self.xxx_interim_shifts is not None else u""


class SignupExtraBase(models.Model):
    signup = models.OneToOneField(Signup, related_name="+", primary_key=True)

    def __unicode__(self):
        return self.signup.__unicode__() if self.signup else 'None'

    @classmethod
    def get_form_class(cls):
        raise NotImplemented('Remember to implement form_class in your SignupExtra class')

    @staticmethod
    def get_query_class():
        return None

    class Meta:
        abstract = True


class EmptySignupExtra(SignupExtraBase):
    @classmethod
    def get_form_class(cls):
        from .forms import EmptySignupExtraForm
        return EmptySignupExtraForm


__all__ = [
    'LabourEventMeta',
    'Job',
    'JobCategory',
    'PersonQualification',
    'Qualification',
    'QualificationExtraBase',
    'Signup',
    'SignupExtraBase',
    'WorkPeriod',
]
