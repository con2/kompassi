import logging

from django.conf import settings
from django.db import models
from django.db.models import Q
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _

from kompassi.core.utils import log_get_or_create

from .email_alias_mixin import EmailAliasMixin

logger = logging.getLogger(__name__)


APP_ALIAS_TEMPLATES = dict(
    core="suunnistajat",
    labour="{event.slug}-tyovoima",
    programme="{event.slug}-ohjelma",
    program_v2="{event.slug}-ohjelma",
    tickets="{event.slug}-liput",
    tickets_v2="{event.slug}-liput",
)


class InternalEmailAlias(EmailAliasMixin, models.Model):
    domain = models.ForeignKey("access.EmailAliasDomain", on_delete=models.CASCADE, verbose_name=_("domain"))

    account_name = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_("account name"),
        help_text="Ennen @-merkkiä tuleva osa sähköpostiosoitetta. Muodostetaan automaattisesti jos tyhjä.",
    )

    target_emails = models.CharField(
        max_length=1023,
        verbose_name=_("target e-mail address"),
        help_text=_("E-mail to this alias will be directed to these e-mail addresses (separated by whitespace)"),
    )

    # denormalized to facilitate searching etc
    email_address = models.CharField(
        max_length=511,
        verbose_name=_("e-mail address"),
        help_text="Muodostetaan automaattisesti",
    )

    event = models.ForeignKey("core.Event", on_delete=models.CASCADE, null=True, blank=True)
    app_label = models.CharField(max_length=63, blank=True)

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("created at"))
    modified_at = models.DateTimeField(auto_now=True, verbose_name=_("updated at"))

    def __str__(self):
        return self.email_address

    def _make_account_name(self):
        return APP_ALIAS_TEMPLATES[self.app_label].format(event=self.event)

    @property
    def normalized_target_emails(self):
        return " ".join(self.target_emails.split() if self.target_emails else [])

    @classmethod
    def ensure_internal_email_aliases(cls):
        from kompassi.core.models import Event

        from .email_alias_domain import EmailAliasDomain

        domains = EmailAliasDomain.objects.filter(has_internal_aliases=True)

        if not domains.exists():
            logger.warning("No EmailAliasDomain with has_internal_aliases=True. Not creating internal aliases.")
            return

        domain = domains.get()

        logger.info("Creating internal e-mail aliases in domain %s", domain)

        alias, created = cls.objects.get_or_create(
            domain=domain,
            app_label="core",
            defaults=dict(
                target_emails="\n".join(email for (name, email) in settings.ADMINS),
            ),
        )

        log_get_or_create(logger, alias, created)

        # Null start times are interpreted to mean "sometime in the future"
        t = now()
        query = Q(start_time__gte=t) | Q(start_time__isnull=True)

        for event in Event.objects.filter(query):
            for app_label in [
                "labour",
                "programme",
                "program_v2",
                "tickets",
                "tickets_v2",
            ]:
                meta = event.get_app_event_meta(app_label)
                if not meta:
                    continue

                plain_contact_email = meta.plain_contact_email
                if not plain_contact_email:
                    logger.warning("Not creating %s internal alias for %s", app_label, event)
                    continue

                alias, created = cls.objects.update_or_create(
                    domain=domain,
                    app_label=app_label,
                    event=event,
                    defaults=dict(
                        target_emails=plain_contact_email,
                    ),
                )
                log_get_or_create(logger, alias, created)

    class Meta:
        verbose_name = _("internal e-mail alias")
        verbose_name_plural = _("internal e-mail aliases")


@receiver(pre_save, sender=InternalEmailAlias)
def populate_email_alias_computed_fields(sender, instance, **kwargs):
    if instance.app_label and not instance.account_name:
        instance.account_name = instance._make_account_name()

    if instance.domain and instance.account_name:
        instance.email_address = instance._make_email_address()
