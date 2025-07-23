from django.db import models
from django.template.defaultfilters import truncatewords
from django.utils.translation import gettext_lazy as _


class ProgrammeFeedback(models.Model):
    programme = models.ForeignKey("programme.Programme", on_delete=models.CASCADE, related_name="feedback")
    author = models.ForeignKey("core.Person", on_delete=models.CASCADE, null=True, blank=True)
    author_ip_address = models.CharField(
        max_length=48,
        blank=True,
        default="",
        verbose_name=_("IP address"),
        help_text=_("The IP address is only visible in the admin interface"),
    )
    author_external_username = models.CharField(
        max_length=150,
        blank=True,
        default="",
        verbose_name=_("External username"),
    )

    is_anonymous = models.BooleanField(
        default=False,
        verbose_name=_("Give feedback anonymously"),
        help_text=_(
            "Unless you choose to give feedback anonymously, your name and e-mail address "
            "will be shared with the programme host and programme manager. Please note that even "
            "if you choose to leave feedback anonymously, abusive feedback can be traced back to "
            "you by the administrator of the system."
        ),
    )
    feedback = models.TextField(verbose_name=_("feedback"))

    created_at = models.DateTimeField(auto_now_add=True)
    hidden_at = models.DateTimeField(null=True)
    hidden_by = models.ForeignKey("auth.User", on_delete=models.CASCADE, null=True, blank=True)

    @property
    def is_visible(self):
        return self.hidden_at is None

    @property
    def author_email(self):
        return self.author.email if self.author else None

    @property
    def is_really_anonymous(self):
        return self.author is None or self.is_anonymous

    @classmethod
    def get_visible_feedback_for_event(cls, event):
        return (
            cls.objects.filter(
                programme__category__event=event,
                hidden_at__isnull=True,
            )
            .select_related("programme")
            .select_related("author")
            .order_by("-created_at")
        )

    def admin_is_visible(self):
        return self.is_visible

    admin_is_visible.short_description = _("visible")
    admin_is_visible.admin_order_field = "hidden_at"
    admin_is_visible.boolean = True

    def admin_get_event(self):
        return self.programme.event if self.programme else None

    admin_get_event.short_description = _("event")
    admin_get_event.admin_order_field = "programme__category__event"

    def admin_get_programme_title(self):
        return self.programme.title if self.programme else None

    admin_get_programme_title.short_description = _("programme")
    admin_get_programme_title.admin_order_field = "programme__title"

    def admin_get_abridged_feedback(self, num_words=20):
        return truncatewords(self.feedback, num_words)

    admin_get_abridged_feedback.short_description = _("feedback")

    class Meta:
        verbose_name = _("programme feedback")
        verbose_name_plural = _("programme feedback")
