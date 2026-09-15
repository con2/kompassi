from core.models.person import Person
from django.contrib.auth.models import User
from graphql_api.language import SupportedLanguageCode, getattr_message_in_language

from kompassi.core.models.email_verification_token import EmailVerificationToken
from kompassi.core.models.password_reset_token import PasswordResetToken

from ..models.registry import Registry
from .section import section


def dump_user(user: User, language: SupportedLanguageCode) -> dict:
    # NOTE: Do not include fields that are duplicate with Person (non-Person Users don't get to dump data anyway)
    # TODO how do we localize this?
    return {
        "Käyttäjätunnus": user.username,
        "Salasana asetettu": user.has_usable_password(),
        "Tili aktiivinen": user.is_active,
        "Pääsy taka-adminiin": user.is_staff,
        "Pääkäyttäjä": user.is_superuser,
        "Tili luotu": user.date_joined.isoformat(),
        "Viimeisin kirjautuminen": user.last_login.isoformat() if user.last_login else None,
    }


def dump_users_registry_data(
    registry: Registry,
    person_or_user: Person | User,
    language: SupportedLanguageCode,
) -> dict:
    person: Person | None
    user: User | None

    if isinstance(person_or_user, User):
        person = person_or_user.person  # type: ignore
        user = person_or_user
    else:
        person = person_or_user
        user = person.user

    if person is None:
        raise ValueError("Person data is required for dumping registry data.")

    return section(
        title=getattr_message_in_language(registry, "title", language),
        content=[
            person.dump_own_data(language) if person else None,
            dump_user(user, language) if user else None,
            *(token.dump_own_data(language) for token in EmailVerificationToken.objects.filter(person=person)),
            *(token.dump_own_data(language) for token in PasswordResetToken.objects.filter(person=person)),
        ],
    )
