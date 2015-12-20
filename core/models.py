# encoding: utf-8

import logging
from datetime import date, datetime, timedelta
from django.core.exceptions import ValidationError

from django.conf import settings
from django.contrib.auth.models import User, Group
from django.db import models
from django.template.loader import render_to_string
from django.utils.dateformat import format as format_date
from django.utils import timezone

from .utils import (
    change_user_password,
    ensure_groups_exist,
    format_date_range,
    pick_attrs,
    SLUG_FIELD_PARAMS,
    url,
    validate_slug,
    slugify,
    event_meta_property,
)


logger = logging.getLogger('kompassi')


class Organization(models.Model):
    slug = models.CharField(**SLUG_FIELD_PARAMS)

    name = models.CharField(max_length=255, verbose_name=u'Nimi')
    name_genitive = models.CharField(max_length=255, verbose_name=u'Nimi genetiivissä')

    description = models.TextField(blank=True, verbose_name=u'Kuvaus')
    homepage_url = models.CharField(blank=True, max_length=255, verbose_name=u'Kotisivu')
    muncipality = models.CharField(
        blank=True,
        max_length=127,
        verbose_name=u'Yhdistyksen kotipaikka',
        help_text=u'Kunta, johon yhdistys on rekisteröity.',
    )
    public = models.BooleanField(
        default=False,
        verbose_name=u'Julkinen',
        help_text=u'Julkisilla yhdistyksillä on yhdistyssivu ja ne näytetään etusivulla.',
    )

    logo_url = models.CharField(
        blank=True,
        max_length=255,
        default='',
        verbose_name=u'Organisaation logon URL',
        help_text=u'Voi olla paikallinen (alkaa /-merkillä) tai absoluuttinen (alkaa http/https)',
    )

    def save(self, *args, **kwargs):
        if self.name and not self.slug:
            self.slug = slugify(self.name)

        if self.name and not self.name_genitive:
            if self.name.endswith(u' ry'):
                self.name_genitive = self.name + u':n'
            else:
                self.name_genitive = self.name + u'n'

        return super(Organization, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name

    @classmethod
    def get_or_create_dummy(cls):
        return cls.objects.get_or_create(
            slug='dummy-organization',
            defaults=dict(
                name='Dummy organization',
                homepage_url='http://example.com',
            )
        )

    @property
    def membership_organization_meta(self):
        if 'membership' not in settings.INSTALLED_APPS:
            return None

        from membership.models import MembershipOrganizationMeta

        try:
            return self.membershiporganizationmeta
        except MembershipOrganizationMeta.DoesNotExist:
            return None

    @property
    def access_organization_meta(self):
        if 'access' not in settings.INSTALLED_APPS:
            return None

        from access.models import AccessOrganizationMeta

        try:
            return self.accessorganizationmeta
        except AccessOrganizationMeta.DoesNotExist:
            return None

    class Meta:
        verbose_name = u'Organisaatio'
        verbose_name_plural = u'Organisaatiot'


class Venue(models.Model):
    name = models.CharField(max_length=63, verbose_name=u'Tapahtumapaikan nimi')
    name_inessive = models.CharField(
        max_length=63,
        verbose_name=u'Tapahtumapaikan nimi inessiivissä',
        help_text=u'Esimerkki: Paasitornissa',
    )

    class Meta:
        verbose_name = u'Tapahtumapaikka'
        verbose_name_plural = u'Tapahtumapaikat'

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.name and not self.name_inessive:
            self.name_inessive = self.name + 'ssa'

        return super(Venue, self).save(*args, **kwargs)

    @classmethod
    def get_or_create_dummy(cls):
        return cls.objects.get_or_create(
            name='Dummy venue'
        )


class Event(models.Model):
    slug = models.CharField(**SLUG_FIELD_PARAMS)

    name = models.CharField(max_length=63, verbose_name=u'Tapahtuman nimi')

    organization = models.ForeignKey(Organization, verbose_name=u'Järjestäjätaho')

    name_genitive = models.CharField(
        max_length=63,
        verbose_name=u'Tapahtuman nimi genetiivissä',
        help_text=u'Esimerkki: Susiconin',
    )

    name_illative = models.CharField(
        max_length=63,
        verbose_name=u'Tapahtuman nimi illatiivissä',
        help_text=u'Esimerkki: Susiconiin',
    )

    name_inessive = models.CharField(
        max_length=63,
        verbose_name=u'Tapahtuman nimi inessiivissä',
        help_text=u'Esimerkki: Susiconissa',
    )

    description = models.TextField(blank=True, verbose_name=u'Kuvaus')

    venue = models.ForeignKey(Venue,
        verbose_name=u'Tapahtumapaikka',
    )

    start_time = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=u'Alkamisaika',
    )

    end_time = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=u'Päättymisaika',
    )

    homepage_url = models.CharField(
        blank=True,
        max_length=255,
        verbose_name=u'Tapahtuman kotisivu',
    )

    public = models.BooleanField(
        default=True,
        verbose_name=u'Julkinen',
        help_text=u'Julkiset tapahtumat näytetään etusivulla.'
    )

    logo_url = models.CharField(
        blank=True,
        max_length=255,
        default='',
        verbose_name=u'Tapahtuman logon URL',
        help_text=u'Voi olla paikallinen (alkaa /-merkillä) tai absoluuttinen (alkaa http/https)',
    )

    description = models.TextField(
        blank=True,
        default='',
        verbose_name=u'Tapahtuman kuvaus',
        help_text=u'Muutaman kappaleen mittainen kuvaus tapahtumasta. Näkyy tapahtumasivulla.',
    )

    class Meta:
        verbose_name = u'Tapahtuma'
        verbose_name_plural = u'Tapahtumat'

    def __init__(self, *args, **kwargs):
        # Avoid having to manually transform 20 or so event setup scripts with organization_name and organization_url
        # in get_or_create.defaults
        if 'organization_name' in kwargs:
            organization_name = kwargs.pop('organization_name')
            organization_url = kwargs.pop('organization_url', u'')

            kwargs['organization'], unused = Organization.objects.get_or_create(
                slug=slugify(organization_name),
                defaults=dict(
                    name=organization_name,
                    homepage_url=organization_url,
                )
            )

        super(Event, self).__init__(*args, **kwargs)

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.name:
            for field, suffix in [
                ('name_genitive', 'in'),
                ('name_illative', 'iin'),
                ('name_inessive', 'issa'),
            ]:
                if not getattr(self, field, None):
                    setattr(self, field, self.name + suffix)

        return super(Event, self).save(*args, **kwargs)

    @property
    def name_and_year(self):
        return u"{name} ({year})".format(
            name=self.name,
            year=self.start_time.year,
        )

    @property
    def formatted_start_and_end_date(self):
        return format_date_range(self.start_time, self.end_time)

    @property
    def headline(self):
        headline_parts = [
            (self.venue.name_inessive if self.venue else None),
            (self.formatted_start_and_end_date if self.start_time and self.end_time else None),
        ]
        headline_parts = [part for part in headline_parts if part]

        return u' '.join(headline_parts)

    @classmethod
    def get_or_create_dummy(cls):
        venue, unused = Venue.get_or_create_dummy()
        organization, unused = Organization.get_or_create_dummy()
        t = timezone.now()

        return cls.objects.get_or_create(
            name='Dummy event',
            defaults=dict(
                venue=venue,
                start_time=t + timedelta(days=60),
                end_time=t + timedelta(days=61),
                slug='dummy',
                organization=organization,
            ),
        )

    labour_event_meta = event_meta_property('labour', 'labour.models:LabourEventMeta')
    programme_event_meta = event_meta_property('programme', 'programme.models:ProgrammeEventMeta')
    badges_event_meta = event_meta_property('badges', 'badges.models:BadgesEventMeta')
    tickets_event_meta = event_meta_property('tickets', 'tickets.models:TicketsEventMeta')
    payments_event_meta = event_meta_property('payments', 'payments.models:PaymentsEventMeta')
    sms_event_meta = event_meta_property('sms', 'sms.models:SMSEventMeta')

    def app_event_meta(self, app_label):
        return getattr(self, '{}_event_meta'.format(app_label))

    def as_dict(self):
        return pick_attrs(self,
            'slug',
            'name',
        )


EMAIL_LENGTH = PHONE_NUMBER_LENGTH = 255
BIRTH_DATE_HELP_TEXT = u'Syntymäaika muodossa {0}'.format(
    format_date(date(1994, 2, 24), settings.DATE_FORMAT)
)
NAME_DISPLAY_STYLE_CHOICES = [
    (u'firstname_nick_surname', u'Etunimi "Nick" Sukunimi'),
    (u'firstname_surname', u'Etunimi Sukunimi'),
    (u'firstname', u'Etunimi'),
    (u'nick', u'Nick'),
]
NAME_DISPLAY_STYLE_FORMATS = dict(
    firstname=u'{self.first_name}',
    firstname_nick_surname=u'{self.first_name} "{self.nick}" {self.surname}',
    firstname_surname=u'{self.first_name} {self.surname}',
    nick=u'{self.nick}',
)


def birth_date_validator(value):
    exc = u"Virheellinen syntymäaika."
    try:
        if value <= date(1900, 1, 1) or value >= date.today():
            raise ValidationError(exc)
        # Following actually also checks that year is >= 1900. Even then, ensure the date can be formatted.
        value.strftime("%Y-%m-%d")
    except ValueError:
        raise ValidationError(exc)


class Person(models.Model):
    first_name = models.CharField(max_length=1023, verbose_name=u'Etunimi')
    official_first_names = models.CharField(
        blank=True,
        max_length=1023,
        verbose_name=u'Viralliset etunimet',
    )
    surname = models.CharField(max_length=1023, verbose_name=u'Sukunimi')
    nick = models.CharField(blank=True, max_length=1023, help_text='Lempi- tai kutsumanimi')
    birth_date = models.DateField(
        null=True,
        blank=True,
        verbose_name=u'Syntymäaika',
        help_text=BIRTH_DATE_HELP_TEXT,
        validators=[birth_date_validator],
    )

    muncipality = models.CharField(
        blank=True,
        max_length=127,
        verbose_name=u'Kotikunta',
        help_text=u'Virallinen kotikuntasi eli kunta jossa olet kirjoilla. Kotikunta ja väestörekisteriin '
            u'merkityt etunimesi (kaikki) ovat pakollisia tietoja, mikäli kuulut '
            u'tai haluat liittyä johonkin yhdistykseen joka käyttää tätä sivustoa jäsenrekisterin '
            u'hallintaan.'
    )

    email = models.EmailField(
        blank=True,
        max_length=EMAIL_LENGTH,
        verbose_name=u'Sähköpostiosoite',
        help_text=u'Sähköposti on ensisijainen yhteydenpitokeino tapahtumaan liittyvissä asioissa.',
    )

    phone = models.CharField(
        blank=True,
        max_length=PHONE_NUMBER_LENGTH,
        verbose_name=u'Puhelinnumero',
        help_text=u'Puhelinnumeroasi käytetään tarvittaessa kiireellisiin yhteydenottoihin koskien osallistumistasi tapahtumaan.',
    )

    may_send_info = models.BooleanField(
        default=False,
        verbose_name=u'Minulle saa lähettää sähköpostitse tietoa tulevista tapahtumista <i>(vapaaehtoinen)</i>',
    )

    allow_work_history_sharing = models.BooleanField(
        default=False,
        verbose_name=u'Työskentelyhistoriani saa näyttää kokonaisuudessaan niille tapahtumille, joihin haen vapaaehtoistyöhön <i>(vapaaehtoinen)</i>',
        help_text=u'Mikäli et anna tähän lupaa, tapahtuman työvoimavastaavalle näytetään ainoastaan työskentelysi aikaisemmissa saman organisaation järjestämissä tapahtumissa.'
    )

    preferred_name_display_style = models.CharField(
        max_length=31,
        verbose_name=u'Nimen esittäminen',
        help_text=u'Tässä voit vaikuttaa siihen, missä muodossa nimesi esitetään (esim. painetaan badgeesi).',
        blank=True,
        choices=NAME_DISPLAY_STYLE_CHOICES,
    )

    notes = models.TextField(blank=True, verbose_name=u'Käsittelijän merkinnät')
    user = models.OneToOneField('auth.User', null=True, blank=True)

    email_verified_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['surname']
        verbose_name = u'Henkilö'
        verbose_name_plural = u'Henkilöt'

    def __unicode__(self):
        return self.full_name

    def clean(self):
        if self.preferred_name_display_style and 'nick' in self.preferred_name_display_style and not self.nick:
            from django.core.exceptions import ValidationError
            raise ValidationError(u'Jos nick on tarkoitus näyttää, se myös täytyy syöttää.')

    @property
    def full_name(self):
        if self.nick:
            style = 'firstname_nick_surname'
        else:
            style = 'firstname_surname'

        return NAME_DISPLAY_STYLE_FORMATS[style].format(self=self)

    @property
    def official_name(self):
        if self.official_first_names:
            first_name = self.official_first_names
        else:
            first_name = self.first_name

        return u"{surname}, {first_name}".format(
            surname=self.surname,
            first_name=first_name,
        )

    @property
    def official_name_short(self):
        return u"{surname}, {first_name}".format(
            surname=self.surname,
            first_name=self.first_name,
        )

    @property
    def official_first_names_or_first_name(self):
        if self.official_first_names:
            return self.official_first_names
        else:
            return self.first_name

    @property
    def name_and_email(self):
        return u"{self.first_name} {self.surname} <{self.email}>".format(self=self)

    @property
    def name_display_style(self):
        if self.preferred_name_display_style:
            return self.preferred_name_display_style
        else:
            if self.nick:
                return 'firstname_nick_surname'
            else:
                return 'firstname_surname'

    @property
    def display_name(self):
        return NAME_DISPLAY_STYLE_FORMATS[self.name_display_style].format(self=self)

    @property
    def username(self):
        return self.user.username if self.user is not None else None

    @property
    def nick_or_first_name(self):
        if 'nick' in self.preferred_name_display_style and self.nick:
            return self.nick
        else:
            return self.first_name

    @classmethod
    def get_or_create_dummy(cls, superuser=True):
        user, unused = User.objects.get_or_create(
            username='mahti',
            defaults=dict(
                first_name='Markku',
                last_name='Mahtinen',
                is_staff=superuser,
                is_superuser=superuser,
            ),
        )

        if not user.password:
            user.set_password('mahti')
            user.save()

        return cls.objects.get_or_create(
            user=user,
            defaults=dict(
                first_name=user.first_name,
                surname=user.last_name,
                nick='Mahti',
                birth_date=date(1984, 1, 1),
                email='mahti@example.com',
                phone='+358 50 555 1234'
            )
        )

    def save(self, *args, **kwargs):
        ret_val = super(Person, self).save(*args, **kwargs)

        if self.user:
            # Update first_name, last_name and email in User if they differ from those in Person
            for person_attr, user_attr in [
                ('first_name', 'first_name'),
                ('surname', 'last_name'),
                ('email', 'email'),
            ]:
                setattr(self.user, user_attr, getattr(self, person_attr))

            self.user.save()

        return ret_val

    @property
    def is_email_verified(self):
        return self.email_verified_at is not None

    @property
    def desuprofile_connection(self):
        if not hasattr(self, '_desuprofile_connection'):
            if 'desuprofile_integration' not in settings.INSTALLED_APPS or self.user is None:
                self._desuprofile_connection = None

            from desuprofile_integration.models import Connection

            try:
                self._desuprofile_connection = Connection.objects.get(user=self.user)
            except Connection.DoesNotExist:
                self._desuprofile_connection = None

        return self._desuprofile_connection

    def get_pending_code(self, CodeModel):
        try:
            return CodeModel.objects.get(person=self, state='valid')
        except CodeModel.DoesNotExist:
            return None

    pending_email_verification = property(
        lambda self: self.get_pending_code(EmailVerificationToken)
    )

    pending_password_reset = property(
        lambda self: self.get_pending_code(PasswordResetToken)
    )

    def setup_code(self, request, CodeModel, **kwargs):
        pending_code = self.get_pending_code(CodeModel)
        if pending_code:
            pending_code.revoke()

        code = CodeModel(person=self, **kwargs)
        code.save()
        code.send(request)

    def setup_email_verification(self, request):
        self.email_verified_at = None
        self.save()

        self.setup_code(request, EmailVerificationToken)

    def setup_password_reset(self, request):
        from ipware.ip import get_real_ip

        self.setup_code(request, PasswordResetToken, ip_address=get_real_ip(request) or '')

    def verify_email(self, code=None):
        if self.is_email_verified:
            raise EmailVerificationError('already_verified')

        if isinstance(code, basestring):
            try:
                code = EmailVerificationToken.objects.get(code=code)
            except EmailVerificationToken.DoesNotExist, e:
                raise EmailVerificationError('invalid_code')

        if code:
            # Verify with a single code. The code needs to be checked.

            if code.person != self:
                raise EmailVerificationError('wrong_person')
            elif code.state != 'valid':
                raise EmailVerificationError('code_not_valid')
            elif code.email != self.email:
                raise EmailVerificationError('email_changed')
            else:
                code.mark_used()
        else:
            # Forcibly verify, regardless of codes.
            EmailVerificationToken.objects.filter(person=self, state='valid').update(state='revoked')

        self.email_verified_at = timezone.now()
        self.save()

    @property
    def is_first_name_visible(self):
        return self.name_display_style in [
            'firstname_nick_surname',
            'firstname_surname',
            'firstname',
        ]

    @property
    def is_surname_visible(self):
        return self.name_display_style in [
            'firstname_nick_surname',
            'firstname_surname',
        ]

    @property
    def is_nick_visible(self):
        return self.name_display_style in [
            'firstname_nick_surname',
            'nick',
        ]

    def as_dict(self):
        return dict(
            pick_attrs(self,
                'first_name',
                'surname',
                'nick',
                'full_name',
                'display_name',
                'preferred_name_display_style',

                'phone',
                'email',
                'birth_date',
            ),

            username=self.user.username if self.user else None,
            groups=[group.name for group in self.user.groups.all()] if self.user else [],
        )

    @classmethod
    def is_user_person(cls, user):
        if user.is_anonymous():
            return False
        else:
            return Person.objects.filter(user=user).exists()


class GroupManagementMixin(object):
    @staticmethod
    def is_user_in_group(user, group):
        if not user.is_authenticated():
            return False

        if user.is_superuser:
            return True

        return user.groups.filter(pk=group.pk).exists()

    def is_user_admin(self, user):
        return self.is_user_in_group(user, self.admin_group)

    @classmethod
    def make_group_name(cls, host, suffix):
        # to avoid cases where someone calls .get_or_create_groups(foo, 'admins')
        # and would otherwise get groups a, d, m, i, n, s...
        assert isinstance(suffix, basestring) and len(suffix) > 1

        from django.contrib.contenttypes.models import ContentType

        ctype = ContentType.objects.get_for_model(cls)

        return '{installation_slug}-{host_slug}-{app_label}-{suffix}'.format(
            installation_slug=settings.KOMPASSI_INSTALLATION_SLUG,
            host_slug=host.slug,
            app_label=ctype.app_label,
            suffix=suffix,
        )

    @classmethod
    def get_or_create_groups(cls, host, suffixes):
        group_names = [cls.make_group_name(host, suffix) for suffix in suffixes]

        return ensure_groups_exist(group_names)


class EventMetaBase(models.Model, GroupManagementMixin):
    event = models.OneToOneField('core.Event', primary_key=True, related_name='%(class)s')
    admin_group = models.ForeignKey('auth.Group')

    class Meta:
        abstract = True

    def get_group(self, suffix):
        group_name = self.make_group_name(self.event, suffix)

        return Group.objects.get(name=group_name)


ONE_TIME_CODE_LENGTH = 40
ONE_TIME_CODE_ALPHABET = '0123456789abcdef'


class OneTimeCode(models.Model):
    code = models.CharField(max_length=63, unique=True)
    person = models.ForeignKey(Person)
    created_at = models.DateTimeField(auto_now_add=True)
    used_at = models.DateTimeField(null=True, blank=True)
    state = models.CharField(
        max_length=8,
        default='valid',
        choices=[
            ('valid', u'Kelvollinen'),
            ('used', u'Käytetty'),
            ('revoked', u'Mitätöity'),
        ]
    )

    @property
    def is_used(self):
        return self.used_at is not None

    def __unicode__(self):
        return self.code

    def save(self, *args, **kwargs):
        if not self.code:
            from random import choice
            self.code = "".join(choice(ONE_TIME_CODE_ALPHABET) for _ in range(ONE_TIME_CODE_LENGTH))

        return super(OneTimeCode, self).save(*args, **kwargs)

    def revoke(self):
        assert self.state == 'valid'
        self.state = 'revoked'
        self.used_at = timezone.now()
        self.save()

    def render_message_subject(self, request):
        raise NotImplemented()

    def render_message_body(self, request):
        raise NotImplemented()

    def send(self, request, **kwargs):
        body = self.render_message_body(request)
        subject = self.render_message_subject(request)

        opts = dict(
            subject=subject,
            body=body,
            to=(self.person.name_and_email,),
        )

        opts.update(kwargs)

        if 'background_tasks' in settings.INSTALLED_APPS:
            from .tasks import send_email
            send_email.delay(**opts)
        else:
            from django.core.mail import EmailMessage

            if settings.DEBUG:
                logger.debug(body)

            EmailMessage(**opts).send(fail_silently=True)

    def mark_used(self):
        assert self.state == 'valid'

        self.used_at = timezone.now()
        self.state = 'used'
        self.save()

    class Meta:
        abstract = True
        index_together = [
            ('person', 'state'),
        ]


class PasswordResetToken(OneTimeCode):
    ip_address = models.CharField(max_length=45, blank=True) # IPv6

    def render_message_subject(self, request):
        return u'{settings.KOMPASSI_INSTALLATION_NAME}: Salasanan vaihto'.format(settings=settings)

    def render_message_body(self, request):
        vars = dict(
            link=request.build_absolute_uri(url('core_password_reset_view', self.code))
        )

        return render_to_string('core_password_reset_message.eml', vars, request=request)

    @classmethod
    def reset_password(cls, code, new_password):
        try:
            code = cls.objects.get(code=code, state='valid')
        except cls.DoesNotExist:
            raise PasswordResetError('invalid_code')

        code.mark_used()

        user = code.person.user

        change_user_password(user, new_password=new_password)


class EmailVerificationToken(OneTimeCode):
    email = models.CharField(max_length=255)

    def save(self, *args, **kwargs):
        if self.person and not self.email:
            self.email = self.person.email

        return super(EmailVerificationToken, self).save(*args, **kwargs)

    def render_message_subject(self, request):
        return u'{settings.KOMPASSI_INSTALLATION_NAME}: Vahvista sähköpostiosoitteesi!'.format(settings=settings)

    def render_message_body(self, request):
        vars = dict(
            link=request.build_absolute_uri(url('core_email_verification_view', self.code))
        )

        return render_to_string('core_email_verification_message.eml', vars, request=request)


class EmailVerificationError(RuntimeError):
    pass


class PasswordResetError(RuntimeError):
    pass


__all__ = [
    'BIRTH_DATE_HELP_TEXT',
    'Event',
    'EventMetaBase',
    'EMAIL_LENGTH',
    'Person',
    'PHONE_NUMBER_LENGTH',
    'Venue',
]
