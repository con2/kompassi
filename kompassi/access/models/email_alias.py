import logging

from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

from kompassi.access.models.email_alias_type import EmailAliasVariant

from .email_alias_mixin import EmailAliasMixin

logger = logging.getLogger(__name__)


class EmailAlias(EmailAliasMixin, models.Model):
    type = models.ForeignKey(
        "access.EmailAliasType", on_delete=models.CASCADE, verbose_name=_("type"), related_name="email_aliases"
    )
    person = models.ForeignKey(
        "core.Person", on_delete=models.CASCADE, verbose_name=_("person"), related_name="email_aliases"
    )

    account_name = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_("account name"),
        help_text="Ennen @-merkkiä tuleva osa sähköpostiosoitetta. Muodostetaan automaattisesti jos tyhjä.",
    )

    # denormalized to facilitate searching etc
    email_address = models.CharField(
        max_length=511,
        verbose_name=_("e-mail address"),
        help_text="Muodostetaan automaattisesti",
    )

    # to facilitate easy pruning of old addresses
    group_grant = models.ForeignKey(
        "access.GroupEmailAliasGrant",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        help_text="Myöntämiskanava antaa kaikille tietyn ryhmän jäsenille tietyntyyppisen sähköpostialiaksen. "
        "Jos aliakselle on asetettu myöntämiskanava, alias on myönnetty tämän myöntämiskanavan perusteella, "
        "ja kun myöntämiskanava vanhenee, kaikki sen perusteella myönnetyt aliakset voidaan poistaa kerralla.",
    )

    # denormalized, for unique_together and easy queries
    domain = models.ForeignKey("access.EmailAliasDomain", on_delete=models.CASCADE, verbose_name=_("domain"))

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("created at"))
    modified_at = models.DateTimeField(auto_now=True, verbose_name=_("updated at"))

    def __str__(self):
        return self.email_address

    @classmethod
    def get_or_create_dummy(cls, variant: EmailAliasVariant = EmailAliasVariant.FIRSTNAME_LASTNAME):
        from kompassi.core.models import Person

        from .email_alias_type import EmailAliasType

        alias_type, unused = EmailAliasType.get_or_create_dummy(variant=variant)
        person, unused = Person.get_or_create_dummy()

        return cls.objects.get_or_create(
            type=alias_type,
            person=person,
        )

    class Meta:
        verbose_name = _("e-mail alias")
        verbose_name_plural = _("e-mail aliases")

        unique_together = [("domain", "account_name")]


@receiver(pre_save, sender=EmailAlias)
def populate_email_alias_computed_fields(sender, instance: EmailAlias, **kwargs):
    if instance.type:
        instance.domain = instance.type.domain

        if instance.person and not instance.account_name:
            instance.account_name = instance.type.variant.get_account_name(instance.person, instance.domain)

        if instance.account_name:
            instance.email_address = instance._make_email_address()
