from __future__ import annotations

import logging
from enum import Enum
from typing import TYPE_CHECKING

from django.db import models

from kompassi.access.utils import emailify

from .email_alias_domain import EmailAliasDomain

if TYPE_CHECKING:
    from kompassi.core.models.person import Person

    from .email_alias import EmailAlias


logger = logging.getLogger(__name__)


class EmailAliasVariant(Enum):
    FIRSTNAME_LASTNAME = "firstname.lastname"
    NICK = "nick"
    CUSTOM = "custom"

    def get_account_name(self, person: Person, domain: EmailAliasDomain):
        match self:
            case EmailAliasVariant.FIRSTNAME_LASTNAME:
                return emailify(f"{person.first_name} {person.surname}")
            case EmailAliasVariant.NICK if person.nick:
                return emailify(person.nick)
            case EmailAliasVariant.NICK:
                return emailify(person.first_name)
            case EmailAliasVariant.CUSTOM:
                return self.get_custom_email_alias(person, domain)
            case _:
                raise NotImplementedError(self)

    def get_custom_email_alias(self, person: Person, domain: EmailAliasDomain):
        from kompassi.labour.models.signup import Signup

        organization = domain.organization
        signup = (
            Signup.objects.filter(
                event__organization=organization,
                person=person,
            )
            .order_by("-created_at")
            .first()
        )
        if signup and (email_alias := getattr(signup.signup_extra, "email_alias", "")):
            try:
                return emailify(email_alias.replace(f"@{domain.domain_name}", ""))
            except Exception:
                logger.error("Failed to emailify tracon person %s", signup, exc_info=True)

        # fallback
        return EmailAliasVariant.NICK.get_account_name(person, domain)


class EmailAliasType(models.Model):
    domain: models.ForeignKey[EmailAliasDomain] = models.ForeignKey(
        EmailAliasDomain,
        on_delete=models.CASCADE,
        verbose_name="domain",
    )

    variant_slug = models.CharField(
        max_length=max(len(variant.name) for variant in EmailAliasVariant),
        choices=[(tag.name, tag.value) for tag in EmailAliasVariant],
        blank=True,
        default="",
    )

    priority = models.IntegerField(
        default=0,
        verbose_name="priority",
        help_text=(
            "When determining the e-mail address of a person in relation to a specific event, the "
            "e-mail alias type with the smallest priority number wins."
        ),
    )

    email_aliases: models.QuerySet[EmailAlias]

    @property
    def variant(self) -> EmailAliasVariant:
        return EmailAliasVariant[self.variant_slug]

    @property
    def metavar(self) -> str:
        return self.variant.value

    @classmethod
    def get_or_create_dummy(cls, variant: EmailAliasVariant = EmailAliasVariant.FIRSTNAME_LASTNAME):
        from .email_alias_domain import EmailAliasDomain

        domain, unused = EmailAliasDomain.get_or_create_dummy()
        return cls.objects.get_or_create(domain=domain, variant_slug=variant.name)

    def admin_get_organization(self):
        return self.domain.organization if self.domain else None

    admin_get_organization.short_description = "organization"  # type: ignore
    admin_get_organization.admin_order_field = "domain__organization"  # type: ignore

    def __str__(self):
        metavar = self.metavar if self.variant_slug else None
        domain_name = self.domain.domain_name if self.domain else None
        return f"{metavar}@{domain_name}"

    def create_alias_for_person(self, person, group_grant=None):
        from .email_alias import EmailAlias

        domain_name = self.domain.domain_name

        existing = EmailAlias.objects.filter(person=person, type=self).first()
        if existing:
            logger.debug(
                "Email alias of type %s already exists for %s",
                self,
                person,
            )
            return existing

        account_name = self.variant.get_account_name(person, self.domain)
        if account_name:
            email_address = f"{account_name}@{domain_name}"

            existing = EmailAlias.objects.filter(email_address=email_address).first()
            if existing:
                logger.warning(
                    "Cross-type collision on email alias %s on type %s for %s",
                    email_address,
                    self,
                    person,
                )
                return existing

            if person.email == email_address:
                logger.warning(
                    "Cannot grant alias %s because user %s has it as their email",
                    email_address,
                    person,
                )
                return None

            logger.info(
                "Granting email alias %s of type %s to %s",
                email_address,
                self,
                person,
            )

            newly_created = EmailAlias(
                person=person,
                type=self,
                account_name=account_name,
                group_grant=group_grant,
            )

            newly_created.save()
            return newly_created
        else:
            logger.warning(
                "Not creating alias of type %s for %s (account name generator said None)",
                self,
                person,
            )
            return None
