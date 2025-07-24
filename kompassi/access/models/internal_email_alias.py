import logging

from django.conf import settings
from django.db import models
from django.db.models import Q
from django.utils.timezone import now

from kompassi.core.utils import log_get_or_create

from .email_alias_mixin import EmailAliasMixin

logger = logging.getLogger(__name__)


INTERNAL_CONTACT_ACCOUNT_NAME = "suunnistajat"  # @kompassi.eu
APP_ALIAS_TEMPLATES = dict(
    labour=["{event_slug}-tyovoima", "{event_slug}-volunteers"],
    program_v2=["{event_slug}-ohjelma", "{event_slug}-program"],
    tickets_v2=["{event_slug}-liput", "{event_slug}-tickets"],
)


class InternalEmailAlias(EmailAliasMixin, models.Model):
    domain = models.ForeignKey(
        "access.EmailAliasDomain",
        on_delete=models.CASCADE,
    )

    account_name = models.CharField(max_length=255)

    target_emails = models.TextField(
        verbose_name="target e-mail addresses",
        help_text="plain addresses separated by whitespace",
    )

    email_address = models.CharField(
        max_length=511,
        help_text="denormalized for search, computed automatically",
    )

    event = models.ForeignKey(
        "core.Event",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    app_label = models.CharField(max_length=63, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = [("domain", "account_name")]

    def __str__(self):
        return self.email_address

    def save(self, **kwargs) -> None:
        if self.domain and self.account_name:
            self.email_address = self._make_email_address()

        super().save(**kwargs)

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

        alias, created = cls.objects.update_or_create(
            domain=domain,
            account_name=INTERNAL_CONTACT_ACCOUNT_NAME,
            defaults=dict(
                app_label="core",
                target_emails="\n".join(email for (name, email) in settings.ADMINS),
            ),
        )

        log_get_or_create(logger, alias, created)

        # Null start times are interpreted to mean "sometime in the future"
        t = now()
        query = Q(start_time__gte=t) | Q(start_time__isnull=True)

        for event in Event.objects.filter(query):
            for app_label, account_name_templates in APP_ALIAS_TEMPLATES.items():
                meta = event.get_app_event_meta(app_label)
                if not meta:
                    continue

                plain_contact_email = meta.plain_contact_email
                if not plain_contact_email:
                    logger.warning("Not creating %s internal alias for %s", app_label, event)
                    continue

                for account_name_template in account_name_templates:
                    account_name = account_name_template.format(event_slug=event.slug)

                    alias, created = cls.objects.update_or_create(
                        domain=domain,
                        account_name=account_name,
                        defaults=dict(
                            event=event,
                            app_label=app_label,
                            target_emails=plain_contact_email,
                        ),
                    )
                    log_get_or_create(logger, alias, created)
