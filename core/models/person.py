import logging
from datetime import date, datetime

import phonenumbers
import vobject

from django.core.exceptions import ValidationError
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.db import models
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _
from django.utils.timezone import now
from django.utils import timezone

from ..utils import pick_attrs, calculate_age, format_phone_number, phone_number_validator
from .constants import (
    EMAIL_LENGTH,
    PHONE_NUMBER_LENGTH,
    BIRTH_DATE_HELP_TEXT,
    NAME_DISPLAY_STYLE_CHOICES,
    NAME_DISPLAY_STYLE_FORMATS,
)


logger = logging.getLogger('kompassi')


def birth_date_validator(value):
    exc = "Virheellinen syntymäaika."
    try:
        if value <= date(1900, 1, 1) or value >= date.today():
            raise ValidationError(exc)
        # Following actually also checks that year is >= 1900. Even then, ensure the date can be formatted.
        value.strftime("%Y-%m-%d")
    except ValueError:
        raise ValidationError(exc)


class Person(models.Model):
    first_name = models.CharField(max_length=1023, verbose_name=_('First name'))
    official_first_names = models.CharField(
        blank=True,
        max_length=1023,
        verbose_name=_('Official first names'),
    )
    surname = models.CharField(max_length=1023, verbose_name=_('Surname'))
    nick = models.CharField(
        blank=True,
        max_length=1023,
        verbose_name=_('Nick name'),
        help_text=_('If you go by a nick name or handle that you want printed in your badge and programme details, enter it here.')
    )
    birth_date = models.DateField(
        null=True,
        blank=True,
        verbose_name='Syntymäaika',
        help_text=BIRTH_DATE_HELP_TEXT,
        validators=[birth_date_validator],
    )

    muncipality = models.CharField(
        blank=True,
        max_length=127,
        verbose_name='Kotikunta',
        help_text='Virallinen kotikuntasi eli kunta jossa olet kirjoilla. Kotikunta ja väestörekisteriin '
            'merkityt etunimesi (kaikki) ovat pakollisia tietoja, mikäli kuulut '
            'tai haluat liittyä johonkin yhdistykseen joka käyttää tätä sivustoa jäsenrekisterin '
            'hallintaan.'
    )

    email = models.EmailField(
        blank=True,
        max_length=EMAIL_LENGTH,
        verbose_name='Sähköpostiosoite',
        help_text='Sähköposti on ensisijainen yhteydenpitokeino tapahtumaan liittyvissä asioissa.',
    )

    phone = models.CharField(
        blank=True,
        max_length=PHONE_NUMBER_LENGTH,
        validators=[phone_number_validator],
        verbose_name='Puhelinnumero',
        help_text='Puhelinnumeroasi käytetään tarvittaessa kiireellisiin yhteydenottoihin koskien osallistumistasi tapahtumaan.',
    )

    may_send_info = models.BooleanField(
        default=False,
        verbose_name='Minulle saa lähettää sähköpostitse tietoa tulevista tapahtumista <i>(vapaaehtoinen)</i>',
    )

    allow_work_history_sharing = models.BooleanField(
        default=False,
        verbose_name='Työskentelyhistoriani saa näyttää kokonaisuudessaan niille tapahtumille, joihin haen vapaaehtoistyöhön <i>(vapaaehtoinen)</i>',
        help_text='Mikäli et anna tähän lupaa, tapahtuman työvoimavastaavalle näytetään ainoastaan työskentelysi aikaisemmissa saman organisaation järjestämissä tapahtumissa.'
    )

    preferred_name_display_style = models.CharField(
        max_length=31,
        verbose_name='Nimen esittäminen',
        help_text='Tässä voit vaikuttaa siihen, missä muodossa nimesi esitetään (esim. painetaan badgeesi).',
        blank=True,
        choices=NAME_DISPLAY_STYLE_CHOICES,
    )

    notes = models.TextField(blank=True, verbose_name='Käsittelijän merkinnät')
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)

    email_verified_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['surname']
        verbose_name = 'Henkilö'
        verbose_name_plural = 'Henkilöt'

    def __str__(self):
        return self.full_name

    def clean(self):
        if self.is_nick_visible and not self.nick:
            raise ValidationError('Jos nick on tarkoitus näyttää, se myös täytyy syöttää.')

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

        return "{surname}, {first_name}".format(
            surname=self.surname,
            first_name=first_name,
        )

    @property
    def official_name_short(self):
        return "{surname}, {first_name}".format(
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
        return "{self.first_name} {self.surname} <{self.email}>".format(self=self)

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
        return self.get_formatted_name()

    def get_formatted_name(self, name_display_style=None):
        if not name_display_style:
            name_display_style = self.name_display_style

        return NAME_DISPLAY_STYLE_FORMATS[name_display_style].format(self=self)

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

    def get_normalized_phone_number(
        self,
        region=settings.KOMPASSI_PHONENUMBERS_DEFAULT_REGION,
        format=settings.KOMPASSI_PHONENUMBERS_DEFAULT_FORMAT
    ):
        """
        Returns the phone number of this Person in a normalized format. If the phone number is invalid,
        this is logged, and the invalid phone number is returned as-is.
        """

        try:
            return format_phone_number(self.phone, region=region, format=format)
        except phonenumbers.NumberParseException:
            logger.exception('Person %s has invalid phone number: %s', self, self.phone)
            return self.phone

    @property
    def normalized_phone_number(self):
        return self.get_normalized_phone_number()

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
        from ipware.ip import get_ip
        from .password_reset_token import PasswordResetToken

        self.setup_code(request, PasswordResetToken, ip_address=get_ip(request) or '')

    def verify_email(self, code=None):
        from .email_verification_token import EmailVerificationToken, EmailVerificationError

        if self.is_email_verified:
            raise EmailVerificationError('already_verified')

        if isinstance(code, str):
            try:
                code = EmailVerificationToken.objects.get(code=code)
            except EmailVerificationToken.DoesNotExist as e:
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

    @property
    def age_now(self):
        return self.get_age_at(date.today())

    def get_events(self, **kwargs):
        from .event import Event

        # have programmes
        q = Q(category__programme__organizers=self)

        # or signups
        q |= Q(signup__person=self)

        # or enrollments
        q |= Q(enrollment__person=self)

        q &= Q(**kwargs)

        return Event.objects.filter(q).distinct()

    def get_age_at(self, the_date):
        if self.birth_date is None:
            return None

        if isinstance(the_date, datetime):
            the_date = the_date.date()

        return calculate_age(self.birth_date, the_date)

    def as_dict(self):
        return dict(
            pick_attrs(self,
                'id',
                'first_name',
                'surname',
                'nick',
                'full_name',
                'display_name',
                'preferred_name_display_style',

                'email',
                'birth_date',

                phone=self.normalized_phone_number,
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

    def apply_state(self):
        """
        While there's no "state" field to apply, this method is similar in purpose and equally bad as
        labour.models.signup:Signup.apply_state and programme.models.Programme:Programme.apply_state.
        It updates certain other models based on the changes in this model.

        In this instance, we check the Badges of the person for all future events in case the user has
        changed their name.
        """
        self.apply_state_sync()
        self.apply_state_async()

    def apply_state_sync(self):
        self.apply_state_update_badges()

    def apply_state_update_badges(self):
        if 'badges' not in settings.INSTALLED_APPS:
            return

        from badges.models import Badge

        # Only touch badges for events in the future
        for badge in self.badges.filter(personnel_class__event__start_time__gte=now()):
            Badge.ensure(person=self, event=badge.personnel_class.event)

    def apply_state_async(self):
        if 'background_tasks' in settings.INSTALLED_APPS:
            from ..tasks import person_apply_state_async
            person_apply_state_async(self.pk)
        else:
            self._apply_state_async()

    def _apply_state_async(self):
        self.apply_state_update_crowd()
        self.apply_state_update_may_send_info_group_membership()

    def apply_state_update_crowd(self):
        if 'crowd_integration' not in settings.INSTALLED_APPS:
            return

        from crowd_integration.utils import update_user
        update_user(self.user)

    def apply_state_update_may_send_info_group_membership(self):
        from ..utils import ensure_user_is_member_of_group
        ensure_user_is_member_of_group(
            user=self.user,
            group=settings.KOMPASSI_MAY_SEND_INFO_GROUP_NAME,
            should_belong_to_group=self.may_send_info and self.is_email_verified,
        )

    def ensure_basic_groups(self):
        """
        Note that this method handles the basic groups only locally.

        If the Crowd integration is active, basic groups will be added in Crowd by
        apply_state_new_user_async.
        """
        for group_name in settings.KOMPASSI_NEW_USER_GROUPS:
            self.user.groups.add(Group.objects.get(name=group_name))

    def apply_state_new_user(self, request, password):
        self.apply_state_new_user_sync(request)
        self.apply_state_new_user_async(password)

    def apply_state_new_user_sync(self, request):
        self.setup_email_verification(request)
        self.ensure_basic_groups()

    def apply_state_new_user_async(self, password):
        if 'background_tasks' in settings.INSTALLED_APPS:
            from ..tasks import person_apply_state_new_user_async
            person_apply_state_new_user_async.delay(self.pk, password)
        else:
            self._apply_state_new_user_async(password)

    def _apply_state_new_user_async(self, password):
        self.crowd_create_user(password)
        self.crowd_sync_groups()

    def crowd_create_user(self, password):
        from crowd_integration.utils import create_user
        create_user(self.user, password)

    def crowd_sync_groups(self):
        """
        Ensures the user has their group membership set also in Crowd. Necessary for new users
        to ensure basic groups, but not usually necessary for existing users because when eg.
        labour changes the groups, it updates Crowd on the fly.

        Really just used for initial groups (most importantly `users`).

        TODO Propagate django-admin group changes to Crowd
        https://docs.djangoproject.com/en/1.10/ref/signals/#m2m-changed
        """
        from crowd_integration.utils import ensure_user_group_membership
        for group in self.user.groups.all():
            ensure_user_group_membership(self.user, group.name)

    def get_email_for_event(self, event):
        from labour.models import Signup

        try:
            return Signup.objects.get(event=event, person=self).email_address
        except Signup.DoesNotExist:
            return self.email

    def as_vcard(self, event=None):
        vcard = vobject.vCard()

        vcard.add('n')
        vcard.n.value = vobject.vcard.Name(family=self.surname, given=self.first_name)

        vcard.add('fn')
        vcard.fn.value = self.firstname_surname

        vcard.add('email')
        vcard.email.value = self.get_email_for_event(event) if event is not None else self.email
        vcard.email.type_param = 'INTERNET'

        vcard.add('tel')
        vcard.tel.value = self.normalized_phone_number
        vcard.tel.type_param = 'cell'

        return vcard.serialize()

    def log_view(self, request, **extra_attrs):
        """
        Logs an instance of this persons' Personally Identifiable Information being viewed by
        another user.
        """
        from event_log.utils import emit
        emit(
            'core.person.viewed',
            person=self,
            request=request,
            **extra_attrs
        )

    @property
    def with_privacy(self):
        if not hasattr(self, '_privacy_adapter'):
            # XXX generify
            from badges.proxies.badge.privacy import BadgePrivacyAdapter
            self._privacy_adapter = BadgePrivacyAdapter(self)
        return self._privacy_adapter
