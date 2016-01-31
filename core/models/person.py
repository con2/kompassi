# encoding: utf-8

import logging
from datetime import date

from django.core.exceptions import ValidationError
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.dateformat import format as format_date
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

from ..utils import pick_attrs
from .constants import (
    EMAIL_LENGTH,
    PHONE_NUMBER_LENGTH,
    BIRTH_DATE_HELP_TEXT,
    NAME_DISPLAY_STYLE_CHOICES,
    NAME_DISPLAY_STYLE_FORMATS,
)


logger = logging.getLogger('kompassi')


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
    first_name = models.CharField(max_length=1023, verbose_name=_(u'First name'))
    official_first_names = models.CharField(
        blank=True,
        max_length=1023,
        verbose_name=_(u'Official first names'),
    )
    surname = models.CharField(max_length=1023, verbose_name=_(u'Surname'))
    nick = models.CharField(blank=True, max_length=1023, help_text=_(u'Nick name'))
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
    user = models.OneToOneField(settings.AUTH_USER_MODEL, null=True, blank=True)

    email_verified_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['surname']
        verbose_name = u'Henkilö'
        verbose_name_plural = u'Henkilöt'

    def __unicode__(self):
        return self.full_name

    def clean(self):
        if self.is_nick_visible and not self.nick:
            raise ValidationError(u'Jos nick on tarkoitus näyttää, se myös täytyy syöttää.')

    @property
    def full_name(self):
        if self.nick:
            style = 'firstname_nick_surname'
        else:
            style = 'firstname_surname'

        return NAME_DISPLAY_STYLE_FORMATS[style].format(self=self)

    @property
    def firstname_surname(self):
        return NAME_DISPLAY_STYLE_FORMATS['firstname_surname'].format(self=self)

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
        User = get_user_model()

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

    @property
    def pending_email_verification(self):
        from .email_verification_token import EmailVerificationToken
        return self.get_pending_code(EmailVerificationToken)

    @property
    def pending_password_reset(self):
        from .password_reset_token import PasswordResetToken
        return self.get_pending_code(PasswordResetToken)

    def setup_code(self, request, CodeModel, **kwargs):
        pending_code = self.get_pending_code(CodeModel)
        if pending_code:
            pending_code.revoke()

        code = CodeModel(person=self, **kwargs)
        code.save()
        code.send(request)

    def setup_email_verification(self, request):
        from .email_verification_token import EmailVerificationToken

        self.email_verified_at = None
        self.save()

        self.setup_code(request, EmailVerificationToken)

    def setup_password_reset(self, request):
        from ipware.ip import get_real_ip
        from .password_reset_token import PasswordResetToken

        self.setup_code(request, PasswordResetToken, ip_address=get_real_ip(request) or '')

    def verify_email(self, code=None):
        from .email_verification_token import EmailVerificationToken, EmailVerificationError

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