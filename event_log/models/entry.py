from django.conf import settings
from django.db import models
from django.db.models import Q
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _


TARGET_FKEY_ATTRS = dict(
    null=True,
    blank=True,
    on_delete=models.SET_NULL,
)


class Entry(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    entry_type = models.CharField(max_length=255)
    context = models.CharField(
        max_length=1024,
        blank=True,
        default='',
        verbose_name=_('Context'),
        help_text=_('The URL of the view in which the event occurred.'),
    )
    ip_address = models.CharField(
        max_length=48,
        blank=True,
        default='',
        verbose_name=_('IP address'),
        help_text=_('The IP address this action was performed from.'),
    )

    # various target fkeys, sparse
    event = models.ForeignKey('core.Event', **TARGET_FKEY_ATTRS)
    person = models.ForeignKey('core.Person', **TARGET_FKEY_ATTRS)
    organization = models.ForeignKey('core.Organization', **TARGET_FKEY_ATTRS)
    feedback_message = models.ForeignKey('feedback.FeedbackMessage', **TARGET_FKEY_ATTRS)
    event_survey_result = models.ForeignKey('surveys.EventSurveyResult', **TARGET_FKEY_ATTRS)
    global_survey_result = models.ForeignKey('surveys.GlobalSurveyResult', **TARGET_FKEY_ATTRS)
    search_term = models.CharField(max_length=255, blank=True, default='')

    @property
    def survey_result(self):
        """
        Shortcut for templates etc. that apply to both GlobalSurveyResults and EventSurveyResults.
        """
        return self.event_survey_result if self.event_survey_result else self.global_survey_result

    def send_updates(self):
        from .subscription import Subscription

        q = Q(entry_type=self.entry_type, active=True)

        # TODO need a more flexible filter solution that does not hard-code these
        # One option would be to specify filter = JSONField in Subscription.
        # Implementing this filter would require a client-side check or one SQL query
        # per Subscription, however, as we query Subscriptions by Entry and not vice versa.

        if self.event:
            # Implement the event filter. Subscriptions without event_filter receive updates from
            # all events. Subscriptions with event_filter receive only updates from that event.
            q &= Q(event_filter=self.event) | Q(event_filter__isnull=True)

        if self.event_survey_result:
            # Implement event survey filter.
            survey = self.event_survey_result.survey
            q &= Q(event_survey_filter=survey) | Q(event_survey_filter__isnull=True)

        if self.job_category_filter:
            # Implement job category filter
            from labour.models import Signup
            signup = Signup.objects.get(event=self.event, person=self.person)
            q &= (
                Q(job_category_filter__in=signup.job_categories.all()) |
                Q(job_category_filter__in=signup.job_categories_accepted.all()) |
                Q(job_category_filter__isnull=True)
            )

        for subscription in Subscription.objects.filter(q):
            subscription.send_update_for_entry(self)

    @property
    def entry_type_metadata(self):
        if not hasattr(self, '_entry_type_metadata'):
            from .. import registry
            self._entry_type_metadata = registry.get(self.entry_type)

        return self._entry_type_metadata

    @property
    def email_reply_to(self):
        meta = self.entry_type_metadata

        if callable(meta.email_reply_to):
            return meta.email_reply_to(self)
        else:
            return meta.email_reply_to

    @property
    def message(self):
        meta = self.entry_type_metadata

        if callable(meta.message):
            return meta.message(self)
        else:
            return meta.message.format(entry=self)

    @property
    def email_subject(self):
        return '[{app_name}] {message}'.format(
            app_name=settings.KOMPASSI_INSTALLATION_NAME,
            message=self.message,
        )

    @property
    def email_body(self):
        meta = self.entry_type_metadata

        if callable(meta.email_body_template):
            return meta.email_body_template(self)
        else:
            return render_to_string(meta.email_body_template, dict(
                entry=self,
                settings=settings,
            ))

    class Meta:
        verbose_name = _('log entry')
        verbose_name_plural = _('log entries')
        ordering = ('-created_at',)
