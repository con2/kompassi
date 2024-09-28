from django.conf import settings
from django.db import models
from django.db.models import JSONField
from django.utils.translation import gettext_lazy as _


class Entry(models.Model):
    """
    Superseded by event_log_v2.models.Entry.
    """

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+",
    )
    entry_type = models.CharField(max_length=255)
    context = models.CharField(
        max_length=1024,
        blank=True,
        default="",
        verbose_name=_("Context"),
        help_text=_("The URL of the view in which the event occurred."),
    )
    ip_address = models.CharField(
        max_length=48,
        blank=True,
        default="",
        verbose_name=_("IP address"),
        help_text=_("The IP address this action was performed from."),
    )

    # various target fkeys, sparse
    event = models.ForeignKey(
        "core.Event",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    person = models.ForeignKey(
        "core.Person",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    organization = models.ForeignKey(
        "core.Organization",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    limit_group = models.ForeignKey(
        "tickets.LimitGroup",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    search_term = models.CharField(max_length=255, blank=True, default="")

    # we should probably have shoved them in a jsonfield in the first place
    other_fields = JSONField(blank=True, default=dict)

    class Meta:
        verbose_name = _("log entry")
        verbose_name_plural = _("log entries")
        ordering = ("-created_at",)
