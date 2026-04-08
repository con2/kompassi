from __future__ import annotations

import logging
from datetime import date, datetime
from functools import cached_property
from typing import TYPE_CHECKING

import phonenumbers
import vobject
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q
from django.http import HttpRequest
from django.utils import timezone
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _

from kompassi.graphql_api.language import DEFAULT_LANGUAGE, SupportedLanguageCode
from kompassi.zombies.tickets.utils import format_date

from ..utils import calculate_age, format_phone_number, phone_number_validator, pick_attrs
from .constants import (
    BIRTH_DATE_HELP_TEXT,
    EMAIL_LENGTH,
    NAME_DISPLAY_STYLE_CHOICES,
    NAME_DISPLAY_STYLE_FORMATS,
    PHONE_NUMBER_LENGTH,
)

if TYPE_CHECKING:
    from kompassi.access.models.email_alias import EmailAlias
    from kompassi.badges.models.badge import Badge
    from kompassi.labour.models.qualifications import PersonQualification


logger = logging.getLogger(__name__)


def birth_date_validator(value):
    exc = "Virheellinen syntymäaika."
    try:
        if value <= date(1900, 1, 1) or value >= date.today():
            raise ValidationError(exc)
        # Following actually also checks that year is >= 1900. Even then, ensure the date can be formatted.
        value.strftime("%Y-%m-%d")
    except ValueError as ve:
        raise ValidationError(exc) from ve


class Person(models.Model):
    first_name = models.CharField(max_length=1023, verbose_name=_("First name"))
    official_first_names = models.CharField(
        blank=True,
        max_length=1023,
        verbose_name=_("Official first names"),
    )
    surname = models.CharField(max_length=1023, verbose_name=_("Surname"))
    nick = models.CharField(
        blank=True,
        max_length=1023,
        verbose_name=_("Nick name"),
        help_text=_(
            "If you go by a nick name or handle that you want printed in your badge and programme details, enter it here."
        ),
    )
    discord_handle = models.CharField(
        blank=True,
        max_length=63,  # actually 32 + 1 + 5 but to be safe
        verbose_name=_("Discord username"),
        help_text=_(
            "Your Discord username (NOTE: not display name). Events may use this to give you roles based on your participation."
        ),
    )
    birth_date = models.DateField(
        null=True,
        blank=True,
        verbose_name="Syntymäaika",
        help_text=BIRTH_DATE_HELP_TEXT,
        validators=[birth_date_validator],
    )

    muncipality = models.CharField(
        blank=True,
        max_length=127,
        verbose_name="Kotikunta",
        help_text="Virallinen kotikuntasi eli kunta jossa olet kirjoilla. Kotikunta ja väestörekisteriin "
        "merkityt etunimesi (kaikki) ovat pakollisia tietoja, mikäli kuulut "
        "tai haluat liittyä johonkin yhdistykseen joka käyttää tätä sivustoa jäsenrekisterin "
        "hallintaan.",
    )

    email = models.EmailField(
        blank=True,
        max_length=EMAIL_LENGTH,
        verbose_name=_("email address"),
        help_text=_("Email is the primary means of contact for event-related matters."),
    )

    phone = models.CharField(
        blank=True,
        max_length=PHONE_NUMBER_LENGTH,
        validators=[phone_number_validator],
        verbose_name=_("phone number"),
        help_text=_("Your phone number is used only for urgent contact regarding your participation in the event."),
    )

    may_send_info = models.BooleanField(
        default=False,
        verbose_name=_("I may be sent information about future events by email <i>(optional)</i>"),
    )

    allow_work_history_sharing = models.BooleanField(
        default=False,
        verbose_name="Työskentelyhistoriani saa näyttää kokonaisuudessaan niille tapahtumille, joihin haen vapaaehtoistyöhön <i>(vapaaehtoinen)</i>",
        help_text="Mikäli et anna tähän lupaa, tapahtuman työvoimavastaavalle näytetään ainoastaan työskentelysi aikaisemmissa saman organisaation järjestämissä tapahtumissa.",
    )

    preferred_name_display_style = models.CharField(
        max_length=31,
        verbose_name="Nimen esittäminen listauksissa",
        help_text="Mikäli sinut mainitaan tapahtuman järjestäjä- tai ohjelmalistauksessa (esim. käsiohjelmassa tai web-sivuilla), voit tässä vaikuttaa siihen miten nimesi esitetään kyseisessä listauksessa.",
        blank=True,
        choices=NAME_DISPLAY_STYLE_CHOICES,
    )

    preferred_badge_name_display_style = models.CharField(
        max_length=31,
        verbose_name="Nimen esittäminen badgessa",
        help_text="Mikäli saat johonkin tapahtumaan nimikoidun henkilökortin (esim. työvoima- tai ohjelmabadgen), voit tässä vaikuttaa siihen miten nimesi esitetään kyseisessä badgessa. Huomaathan kuitenkin, että jotkin tapahtumat saattavat vaatia etu- ja sukunimen painamista badgeen, jolloin tämä kenttä vaikuttaa ainoastaan siihen painetaanko badgeen myös nickisi vai ei.",
        blank=True,
        choices=NAME_DISPLAY_STYLE_CHOICES,
    )

    notes = models.TextField(blank=True, verbose_name="Käsittelijän merkinnät")
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)

    email_verified_at = models.DateTimeField(null=True, blank=True)

    badges: models.QuerySet[Badge]
    qualifications: models.QuerySet[PersonQualification]  # XXX naming
    email_aliases: models.QuerySet[EmailAlias]
    user_id: int
    id: int
    pk: int

    class Meta:
        ordering = ["surname"]
        verbose_name = "Henkilö"
        verbose_name_plural = "Henkilöt"

    def __str__(self):
        return self.full_name

    def clean(self):
        if not self.nick and (
            "nick" in self.preferred_name_display_style or "nick" in self.preferred_badge_name_display_style
        ):
            raise ValidationError("Jos nick on tarkoitus näyttää, se myös täytyy syöttää.")

    @property
    def full_name(self):
        if self.nick:
            style = "firstname_nick_surname"
        else:
            style = "firstname_surname"

        return NAME_DISPLAY_STYLE_FORMATS[style].format(self=self)

    @property
    def firstname_surname(self):
        return NAME_DISPLAY_STYLE_FORMATS["firstname_surname"].format(self=self)

    @property
    def official_name(self):
        if self.official_first_names:
            first_name = self.official_first_names
        else:
            first_name = self.first_name

        return f"{self.surname}, {first_name}"

    @property
    def official_name_short(self):
        return f"{self.surname}, {self.first_name}"

    @property
    def official_first_names_or_first_name(self):
        if self.official_first_names:
            return self.official_first_names
        else:
            return self.first_name

    @property
    def name_and_email(self):
        return f"{self.first_name} {self.surname} <{self.email}>"

    def get_name_display_style(self, preferred_name_display_style):
        if preferred_name_display_style:
            return preferred_name_display_style
        elif self.nick:
            return "firstname_nick_surname"
        else:
            return "firstname_surname"

    @property
    def name_display_style(self):
        return self.get_name_display_style(self.preferred_name_display_style)

    @property
    def badge_name_display_style(self):
        return self.get_name_display_style(self.preferred_badge_name_display_style)

    @property
    def display_name(self):
        return self.get_formatted_name()

    def get_formatted_name(self, name_display_style=None):
        if not name_display_style:
            name_display_style = self.name_display_style

        return NAME_DISPLAY_STYLE_FORMATS[name_display_style].format(self=self)

    @property
    def is_first_name_visible(self):
        return "firstname" in self.name_display_style

    @property
    def is_surname_visible(self):
        return "surname" in self.name_display_style

    @property
    def is_nick_visible(self):
        return "nick" in self.name_display_style

    @property
    def username(self):
        return self.user.username if self.user is not None else None

    @property
    def nick_or_first_name(self):
        if "nick" in self.preferred_name_display_style and self.nick:
            return self.nick
        else:
            return self.first_name

    @classmethod
    def get_or_create_dummy(cls, superuser=True, another=False):
        User = get_user_model()

        if another:
            username = "another"
            first_name = "Matti"
            last_name = "Meikäläinen"
            nick = "Masa666"
        else:
            username = "mahti"
            first_name = "Markku"
            last_name = "Mahtinen"
            nick = "Mahti"

        user, unused = User.objects.get_or_create(
            username=username,
            defaults=dict(
                first_name=first_name,
                last_name=last_name,
                is_staff=superuser,
                is_superuser=superuser,
            ),
        )

        if not user.password:
            user.set_password("mahti")
            user.save()

        return cls.objects.get_or_create(
            user=user,
            defaults=dict(
                first_name=user.first_name,  # type: ignore
                surname=user.last_name,  # type: ignore
                nick=nick,
                birth_date=date(1984, 1, 1),
                email=f"{username}@example.com",
                phone="+358 50 555 1234",
                email_verified_at=now(),
            ),
        )

    def save(self, *args, **kwargs):
        ret_val = super().save(*args, **kwargs)

        if self.user:
            # Update first_name, last_name and email in User if they differ from those in Person
            for person_attr, user_attr in [
                ("first_name", "first_name"),
                ("surname", "last_name"),
                ("email", "email"),
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
        format=settings.KOMPASSI_PHONENUMBERS_DEFAULT_FORMAT,
    ):
        """
        Returns the phone number of this Person in a normalized format. If the phone number is invalid,
        this is logged, and the invalid phone number is returned as-is.
        """

        try:
            return format_phone_number(self.phone, region=region, format=format)
        except phonenumbers.NumberParseException:
            return self.phone

    @property
    def normalized_phone_number(self):
        return self.get_normalized_phone_number()

    @cached_property
    def desuprofile_connection(self):
        from kompassi.desuprofile_integration.models import Connection

        if self.user is None:
            return None

        try:
            return Connection.objects.get(user=self.user)
        except Connection.DoesNotExist:
            return None

    def get_pending_code(self, CodeModel):
        try:
            return CodeModel.objects.get(person=self, state="valid")
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

    def setup_email_verification(
        self,
        request: HttpRequest,
        language: SupportedLanguageCode = DEFAULT_LANGUAGE,
    ):
        from .email_verification_token import EmailVerificationToken

        self.email_verified_at = None
        self.save()

        self.setup_code(request, EmailVerificationToken, language=language)

    def setup_password_reset(
        self,
        request: HttpRequest,
        language: SupportedLanguageCode = DEFAULT_LANGUAGE,
    ):
        from kompassi.core.utils import get_ip

        from .password_reset_token import PasswordResetToken

        self.setup_code(
            request,
            PasswordResetToken,
            language=language,
            ip_address=get_ip(request),
        )

    def verify_email(self, code: str | None):
        """
        Verify this users's email. If code is provided, it must match a valid EmailVerificationToken.
        Note that a verified email may also be verified again. This is useful for claiming new orders
        made while not logged in.
        """
        from kompassi.tickets_v2.models.order import Order

        from .email_verification_token import EmailVerificationError, EmailVerificationToken

        if not self.user:
            raise EmailVerificationError("no_user")

        if code:
            try:
                code_instance = EmailVerificationToken.objects.get(code=code)
            except EmailVerificationToken.DoesNotExist as dne:
                raise EmailVerificationError("invalid_code") from dne

            # Verify with a single code. The code needs to be checked.
            if code_instance.person != self:
                raise EmailVerificationError("wrong_person")
            if code_instance.state != "valid":
                raise EmailVerificationError("code_not_valid")
            if code_instance.email != self.email:
                raise EmailVerificationError("email_changed")

            code_instance.mark_used()
        else:
            # Forcibly verify, regardless of codes.
            pass

        self.email_verified_at = timezone.now()
        self.save()

        # Mark other pending verification codes as revoked
        EmailVerificationToken.objects.filter(person=self, state="valid").update(state="revoked")

        # Claim all unclaimed orders with this email address
        Order.objects.filter(
            owner=None,
            email=self.email,
        ).update(
            owner=self.user,
        )

    @property
    def age_now(self):
        return self.get_age_at(date.today())

    def get_events(self, **kwargs):
        from .event import Event

        # have programmes
        q = Q(category__programme__organizers=self)

        # or signups
        q |= Q(signup__person=self)

        # or archived signups
        q |= Q(archived_signups__person=self)

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
        """
        Used by legacy /api/v2/people/me endpoint.
        /oidc/userinfo endpoint contents defined at api_v2.custom_oauth2_validator.
        """
        return dict(
            pick_attrs(
                self,
                "id",
                "first_name",
                "surname",
                "nick",
                "full_name",
                "display_name",
                "preferred_name_display_style",
                "email",
                "birth_date",
                phone=self.normalized_phone_number,
            ),
            username=self.user.username if self.user else None,
            groups=[group.name for group in self.user.groups.all()] if self.user else [],
        )

    @classmethod
    def is_user_person(cls, user):
        if user.is_anonymous:
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

        self.apply_state_update_badges()
        self.apply_state_update_may_send_info_group_membership()

    def apply_state_update_badges(self):
        from kompassi.badges.models import Badge

        # Only touch badges for events in the future
        for badge in self.badges.filter(personnel_class__event__start_time__gte=now()):
            Badge.ensure(person=self, event=badge.personnel_class.event)

    def apply_state_update_may_send_info_group_membership(self):
        from ..utils import ensure_user_is_member_of_group

        ensure_user_is_member_of_group(
            user=self.user,
            group=settings.KOMPASSI_MAY_SEND_INFO_GROUP_NAME,
            should_belong_to_group=self.may_send_info and self.is_email_verified,
        )

    def ensure_basic_groups(self):
        if not self.user:
            raise AssertionError("self.user")
        for group_name in settings.KOMPASSI_NEW_USER_GROUPS:
            self.user.groups.add(Group.objects.get(name=group_name))

    def apply_state_new_user(self, request, password):
        self.setup_email_verification(request)
        self.ensure_basic_groups()

    def get_email_for_event(self, event):
        from kompassi.labour.models import Signup

        try:
            return Signup.objects.get(event=event, person=self).email_address
        except Signup.DoesNotExist:
            return self.email

    def as_vcard(self, event=None):
        vcard = vobject.vCard()

        vcard.add("n")
        vcard.n.value = vobject.vcard.Name(family=self.surname, given=self.first_name)  # type: ignore

        vcard.add("fn")
        vcard.fn.value = self.firstname_surname

        if self.nick:
            vcard.add("nickname")
            vcard.nickname.value = self.nick

        vcard.add("email")
        vcard.email.value = self.get_email_for_event(event) if event is not None else self.email
        vcard.email.type_param = "INTERNET"

        vcard.add("tel")
        vcard.tel.value = self.normalized_phone_number
        vcard.tel.type_param = "cell"

        return vcard.serialize()

    def log_view(self, request):
        """
        Logs an instance of this persons' Personally Identifiable Information being viewed by
        another user.
        """
        from kompassi.event_log_v2.utils.emit import emit

        emit("core.person.viewed", person=self.pk, request=request)

    @property
    def with_privacy(self):
        if not hasattr(self, "_privacy_adapter"):
            # XXX generify
            from kompassi.badges.proxies.badge.privacy import BadgePrivacyAdapter

            self._privacy_adapter = BadgePrivacyAdapter(self)
        return self._privacy_adapter

    def dump_own_data(self, language: SupportedLanguageCode) -> dict:
        # TODO how do we localize this?
        return {
            "ID": self.id,
            "Etunimi": self.first_name,
            "Sukunimi": self.surname,
            "Nick": self.nick,
            "Syntymäaika": format_date(self.birth_date) if self.birth_date else None,
            "Sähköposti": self.email,
            "Puhelin": self.normalized_phone_number,
            "Discord": self.discord_handle,
            "Kotikunta": self.muncipality,
            "Viralliset etunimet": self.official_first_names,
            "Sähköposti vahvistettu": self.is_email_verified,
            "Saa lähettää tietoa tulevista tapahtumista": self.may_send_info,
            "Työskentelyhistorian saa jakaa muiden tapahtumien kanssa": self.allow_work_history_sharing,
            "Nimen esitystapa listauksissa": self.get_name_display_style_display(),  # type: ignore
            "Nimen esitystapa badgeissa": self.get_badge_name_display_style_display(),  # type: ignore
        }
