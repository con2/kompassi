# encoding: utf-8

from datetime import date, datetime, timedelta

from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.timezone import now

from core.csv_export import CsvExportMixin
from core.models import EventMetaBase
from core.utils import (
    alias_property,
    ensure_user_is_member_of_group,
    ensure_user_is_not_member_of_group,
    is_within_period,
    SLUG_FIELD_PARAMS,
    NONUNIQUE_SLUG_FIELD_PARAMS,
    slugify,
    time_bool_property,
)


GROUP_VERBOSE_NAMES_BY_SUFFIX = dict(
    admins=u'Työvoimavastaavat',
    applicants=u'Aktiiviset',
    new=u'Uudet hakijat',
    processed=u'Käsitellyt',
    accepted=u'Hyväksytyt',
    finished=u'Työvuorotetut',
    complained=u'Reklamoidut',
    cancelled=u'Peruutetut',
    rejected=u'Hylätyt',
    arrived=u'Saapuneet',
    workaccepted=u'Työnsä hyväksytysti suorittaneet',
    reprimanded=u'Työnsä moitittavasti suorittaneet',
)


SIGNUP_STATE_GROUPS = [
    'applicants',
    'new',
    'processed',
    'accepted',
    'finished',
    'complained',
    'cancelled',
    'rejected',
    'arrived',
    'workaccepted',
    'reprimanded',
]


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

    signup_message = models.TextField(
        null=True,
        blank=True,
        default=u'',
        verbose_name=u'Ilmoittautumisen huomautusviesti',
        help_text=u'Tämä viesti näytetään kaikille työvoimailmoittautumisen alussa. Käytettiin '
            u'esimerkiksi Tracon 9:ssä kertomaan, että työvoimahaku on avoinna enää JV:ille ja '
            u'erikoistehtäville.',
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
        admin_group, unused = LabourEventMeta.get_or_create_group(event, 'admins')

        t = now()

        labour_event_meta, created = cls.objects.get_or_create(
            event=event,
            defaults=dict(
                admin_group=admin_group,
                signup_extra_content_type=content_type,
                registration_opens=t - timedelta(days=60),
                registration_closes=t + timedelta(days=60),
                work_begins=event.start_time - timedelta(days=1),
                work_ends=event.end_time + timedelta(days=1),
                contact_email='dummy@example.com',
                monitor_email='dummy@example.com',
            )
        )

        labour_event_meta.create_groups()

        return labour_event_meta, created

    @classmethod
    def get_or_create_group(cls, event, suffix):
        if isinstance(suffix, (str, unicode)):
            verbose_name = GROUP_VERBOSE_NAMES_BY_SUFFIX[suffix]
        else:
            verbose_name = suffix.name
            suffix = suffix.slug

        group, created = super(LabourEventMeta, cls).get_or_create_group(event, suffix)

        if 'mailings' in settings.INSTALLED_APPS:
            from mailings.models import RecipientGroup

            RecipientGroup.objects.get_or_create(
                event=event,
                app_label='labour',
                group=group,
                defaults=dict(
                    verbose_name=verbose_name,
                ),
            )

        return group, created

    def create_groups(self):
        for group_suffix in SIGNUP_STATE_GROUPS:
            group, created = LabourEventMeta.get_or_create_group(self.event, group_suffix)

        for job_category in JobCategory.objects.filter(event=self.event):
            group, created = LabourEventMeta.get_or_create_group(self.event, job_category)

    @property
    def is_registration_open(self):
        return is_within_period(self.registration_opens, self.registration_closes)

    def is_person_signed_up(self, person):
        return Signup.objects.filter(person=person, event=self.event).exists()

    def get_signup_for_person(self, person):
        try:
            return Signup.objects.get(person=person, event=self.event)
        except Signup.DoesNotExist:
            return Signup(person=person, event=self.event)

    @property
    def work_hours(self):
        from programme.utils import full_hours_between
        return full_hours_between(self.work_begins, self.work_ends)

    @property
    def applicants_group(self):
        return self.get_group('applicants')

    @property
    def accepted_group(self):
        return self.get_group('accepted')

    @property
    def finished_group(self):
        return self.get_group('finished')

    @property
    def rejected_group(self):
        return self.get_group('rejected')


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
    slug = models.CharField(**dict(NONUNIQUE_SLUG_FIELD_PARAMS))

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

        unique_together = [
            ('event', 'slug'),
        ]

    def __unicode__(self):
        return self.name

    @classmethod
    def get_or_create_dummies(cls):
        from core.models import Event
        event, unused = Event.get_or_create_dummy()
        jc1, unused = cls.objects.get_or_create(event=event, name='Dummy 1', slug='dummy-1')
        jc2, unused = cls.objects.get_or_create(event=event, name='Dummy 2', slug='dummy-2')

        return [jc1, jc2]

    def save(self, *args, **kwargs):
        if self.slug is None and self.name is not None:
            self.slug = slugify(self.name)

        return super(JobCategory, self).save(*args, **kwargs)


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


class AlternativeSignupForm(models.Model):
    """
    Most workers are registered using the default form. However, some workers are "special",
    such as the organizers (ConCom). We would still like to get their Signups, but they do not
    need to answer all the stupid questions - just some of them.

    This model represents an alternative form that some of these "special" workers can use to sign
    up. Access to this alternative form is controlled using the link. If you know the URL, you can
    use the form.

    Instances of AlternativeSignupForm are supposed to be installed in the database by a setup
    script. For examples, see `tracon9/management/commands/setup_tracon.py` and look for
    AlternativeSignupForm.

    The actual form classes should inherit from django.forms.ModelForm and
    labour.forms.AlternativeFormMixin. For examples, see `tracon9/forms.py` and look for
    OrganizerSignupForm and OrganizerSignupExtraForm.
    """

    event = models.ForeignKey('core.Event', verbose_name=u'Tapahtuma')

    slug = models.CharField(**NONUNIQUE_SLUG_FIELD_PARAMS)

    title = models.CharField(
        max_length=63,
        verbose_name=u'Otsikko',
        help_text=u'Tämä otsikko näkyy käyttäjälle.'
    )

    signup_form_class_path = models.CharField(
        max_length=63,
        help_text=u'Viittaus ilmoittautumislomakkeen toteuttavaan luokkaan. Esimerkki: tracon9.forms:ConcomSignupForm',
    )

    signup_extra_form_class_path = models.CharField(
        max_length=63,
        default='labour.forms:EmptySignupExtraForm',
        help_text=u'Viittaus lisätietolomakkeen toteuttavaan luokkaan. Esimerkki: tracon9.forms:ConcomSignupExtraForm',
    )

    active_from = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=u'Käyttöaika alkaa',
    )

    active_until = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=u'Käyttöaika päättyy',
    )

    signup_message = models.TextField(
        null=True,
        blank=True,
        default=u'',
        verbose_name=u'Ilmoittautumisen huomautusviesti',
        help_text=u'Tämä viesti näytetään kaikille tätä lomaketta käyttäville työvoimailmoittautumisen alussa. Käytettiin '
            u'esimerkiksi Tracon 9:ssä kertomaan, että työvoimahaku on avoinna enää JV:ille ja '
            u'erikoistehtäville.',
    )

    def __unicode__(self):
        return self.title

    @property
    def signup_form_class(self):
        if not getattr(self, '_signup_form_class', None):
            from core.utils import get_code
            self._signup_form_class = get_code(self.signup_form_class_path)

        return self._signup_form_class

    @property
    def signup_extra_form_class(self):
        if not getattr(self, '_signup_extra_form_class', None):
            from core.utils import get_code
            self._signup_extra_form_class = get_code(self.signup_extra_form_class_path)

        return self._signup_extra_form_class

    @property
    def is_active(self):
        return is_within_period(self.active_from, self.active_until)

    class Meta:
        verbose_name = u'Vaihtoehtoinen ilmoittautumislomake'
        verbose_name_plural = u'Vaihtoehtoiset ilmoittautumislomakkeet'
        unique_together = [
            ('event', 'slug'),
        ]




class PersonnelClass(models.Model):
    event = models.ForeignKey(Event)
    app_label = models.CharField(max_length=63, blank=True, default="")
    name = models.CharField(max_length=63)
    slug = models.CharField(**NONUNIQUE_SLUG_FIELD_PARAMS)
    perks = models.ManyToManyField(Perk, blank=True)
    priority = models.IntegerField(default=0)

    class Meta:
        verbose_name = u'henkilöstöluokka'
        verbose_name_plural = u'henkilöstöluokat'

        unique_together = [
            ('event', 'slug'),
        ]

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.name and not self.slug:
            self.slug = slugify(self.name)

        return super(PersonnelClass, self).save(*args, **kwargs)


NUM_FIRST_CATEGORIES = 5
SIGNUP_STATE_NAMES = dict(
    new=u'Uusi',
    accepted=u'Hyväksytty, odottaa vuoroja',
    finished=u'Hyväksytty, vuorot lähetetty',
    complained=u'Hyväksytty, vuorot lähetetty, vuoroista reklamoitu',

    rejected=u'Hylätty (työvoimavastaava ei hyväksynyt töihin)',
    cancelled=u'Peruutettu (hakijan itsensä peruma)',

    arrived=u'Saapunut tapahtumaan',

    honr_discharged=u'Työpanos suoritettu hyväksytysti',
    dish_discharged=u'Työpanoksessa moitittavaa',
    no_show=u'Jätti saapumatta paikalle',
    relieved=u'Vapautettu tehtävästään',

    beyond_logic=u'Perätilassa (irrotettu kaikesta automaattisesta käsittelystä)',
)

SIGNUP_STATE_CLASSES = dict(
    new=u'default',
    accepted=u'info',
    finished=u'success',
    complained=u'warning',
    rejected=u'danger',
    cancelled=u'danger',
    arrived=u'success',
    honr_discharged=u'success',
    dish_discharged=u'danger',
    no_show=u'danger',
    beyond_logic=u'danger',
    relieved=u'danger',
)
SIGNUP_STATE_LABEL_CLASSES = dict(
    (state_name, "label-{generic_class}".format(generic_class=generic_class))
    for (state_name, generic_class) in SIGNUP_STATE_CLASSES.iteritems()
)
SIGNUP_STATE_BUTTON_CLASSES = dict(
    (state_name, "btn-{generic_class}".format(generic_class=generic_class))
    for (state_name, generic_class) in SIGNUP_STATE_CLASSES.iteritems()
)
SIGNUP_STATE_DESCRIPTIONS = dict(
    new=u'Hakemuksesi on vastaanotettu, ja työvoimavastaavat käsittelevät sen lähiaikoina. Saat tiedon hakemuksesi hyväksymisestä tai hylkäämisestä sähköpostitse.',
    accepted=u'Työvoimavastaavat ovat alustavasti hyväksyneet sinut vapaaehtoistyöhön tähän tapahtumaan, mutta sinulle ei ole vielä määritelty työvuoroja. Saat tiedon työvuoroistasi myöhemmin sähköpostitse.',
)
SIGNUP_STATE_IMPERATIVES = dict(
    new=u'Palauta tilaan Uusi',
    accepted=u'Hyväksy hakemus',
    finished=u'Lähetä vuorot',
    arrived=u'Merkitse saapuneeksi',
    complained=u'Kirjaa reklamaatio vuoroista',
    honr_discharged=u'Teki työnsä hyväksytysti',
    dish_discharged=u'Teki työnsä moitittavasti',
    no_show=u'Ei saapunut paikalle',
    relieved=u'Vapauta tehtävästään',
    rejected=u'Hylkää',
    cancelled=u'Merkitse peruutetuksi',
    beyond_logic=u'Aseta perätilaan',
)

STATE_FLAGS_BY_NAME = dict(
    #                active accept ready  compla arrive workac reprim reject cancel
    new=            (True,  False, False, False, False, False, False, False, False),
    accepted=       (True,  True,  False, False, False, False, False, False, False),
    finished=       (True,  True,  True,  False, False, False, False, False, False),
    complained=     (True,  True,  True,  True,  False, False, False, False, False),
    arrived=        (True,  True,  True,  False, True,  False, False, False, False),
    honr_discharged=(True,  True,  True,  False, True,  True,  False, False, False),
    dish_discharged=(True,  True,  True,  False, True,  False, True,  False, False),
    no_show=        (True,  True,  True,  False, False, False, True,  False, False),
    rejected=       (False, False, False, False, False, False, False, True,  False),
    relieved=       (False, True,  False, False, False, False, False, False, True ),
    cancelled=      (False, False, False, False, False, False, False, False, True ),
    beyond_logic=   (False, False, False, False, False, False, False, False, False),
)

STATE_NAME_BY_FLAGS = dict((flags, name) for (name, flags) in STATE_FLAGS_BY_NAME.iteritems())

STATE_TIME_FIELDS = [
    'created_at',
    'time_accepted',
    'time_finished',
    'time_complained',
    'time_cancelled',
    'time_rejected',
    'time_arrived',
    'time_work_accepted',
    'time_reprimanded',
]


class Signup(models.Model, CsvExportMixin):
    person = models.ForeignKey('core.Person')
    event = models.ForeignKey('core.Event')

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
        verbose_name=u'Hyväksytyt tehtäväalueet',
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

    alternative_signup_form_used = models.ForeignKey(AlternativeSignupForm,
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
    is_processed = property(lambda self: self.state != 'new')

    class Meta:
        verbose_name = u'ilmoittautuminen'
        verbose_name_plural=u'ilmoittautumiset'

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
            return u'Vänkäri'

    @classmethod
    def get_or_create_dummy(cls):
        from core.models import Person, Event

        person, unused = Person.get_or_create_dummy()
        event, unused = Event.get_or_create_dummy()

        signup, created = Signup.objects.get_or_create(person=person, event=event)
        extra = signup.signup_extra
        extra.save()

        return signup, created

    def apply_state(self):
        if 'background_tasks' in settings.INSTALLED_APPS:
            from .tasks import signup_apply_state
            signup_apply_state.delay(self.pk)
        else:
            self._apply_state()

    def _apply_state(self):
        self.apply_group_membership()
        self.send_messages()
        self.ensure_badge_exists_if_necessary()

    def apply_group_membership(self):
        for group_suffix in SIGNUP_STATE_GROUPS:
            should_belong_to_group = getattr(self, 'is_{group_suffix}'.format(group_suffix=group_suffix))
            group = self.event.labour_event_meta.get_group(group_suffix)

            ensure_user_is_member_of_group(self.person.user, group, should_belong_to_group)

        for job_category in JobCategory.objects.filter(event=self.event):
            should_belong_to_group = self.job_categories_accepted.filter(pk=job_category.pk).exists()
            group = self.event.labour_event_meta.get_group(job_category.slug)

            ensure_user_is_member_of_group(self.person.user, group, should_belong_to_group)

    def send_messages(self, resend=False):
        if 'mailings' not in settings.INSTALLED_APPS:
            return

        from mailings.models import Message
        Message.send_messages(self.event, 'labour', self.person)

    def ensure_badge_exists_if_necessary(self):
        if 'badges' not in settings.INSTALLED_APPS:
            return

        if self.event.badges_event_meta is None:
            return

        if not self.is_accepted:
            return

        # TODO revoke badge if one exists but shouldn't

        from badges.models import Badge
        Badge.get_or_create(event=self.event, person=self.person)

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
    def _state_flags(self):
        return (
            self.is_active,
            self.is_accepted,
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
        (
            self.is_active,
            self.is_accepted,
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
            states.extend(('finished', 'cancelled'))
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
    def applicant_can_cancel(self):
        return self.is_active and not self.is_cancelled and not self.is_rejected and \
            not self.is_arrived

    @property
    def formatted_job_categories_accepted(self):
        return format_job_categories(self.job_categories_accepted.all())

    @property
    def formatted_job_categories(self):
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


class InfoLink(models.Model):
    event = models.ForeignKey('core.Event', verbose_name=u'Tapahtuma')
    group = models.ForeignKey('auth.Group',
        verbose_name=u'Ryhmä',
        help_text=u'Linkki näytetään vain tämän ryhmän jäsenille.',
    )

    url = models.CharField(
        max_length=255,
        verbose_name=u'Osoite',
        help_text=u'Muista aloittaa ulkoiset linkit <i>http://</i> tai <i>https://</i>.'
    )

    title = models.CharField(max_length=255, verbose_name=u'Teksti')

    class Meta:
        verbose_name = u'työvoimaohje'
        verbose_name_plural = u'työvoimaohjeet'

    def __unicode__(self):
        return self.title


__all__ = [
    'AlternativeSignupForm',
    'InfoLink',
    'Job',
    'JobCategory',
    'LabourEventMeta',
    'PersonQualification',
    'Qualification',
    'QualificationExtraBase',
    'Signup',
    'SignupExtraBase',
    'WorkPeriod',
]
