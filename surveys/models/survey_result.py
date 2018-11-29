from collections import Iterable

from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils.translation import ugettext_lazy as _

from core.csv_export import CsvExportMixin


class SurveyResult(CsvExportMixin, models.Model):
    # Subclasses must provide a `survey` field
    # survey = models.ForeignKey(..., on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)

    model = JSONField()

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    author_ip_address = models.CharField(
        max_length=48,
        blank=True,
        default='',
        verbose_name=_('IP address'),
    )

    def get_csv_fields(self, event):
        assert event == self.event
        return [(self.__class__, field_name) for field_name in self.survey.field_names]

    def get_csv_row(self, event, fields, m2m_mode='comma_separated'):
        assert event == self.event
        assert m2m_mode == 'comma_separated'

        def _generator():
            for (cls, field_name) in fields:
                value = self.model.get(field_name)
                if isinstance(value, Iterable) and not isinstance(value, str):
                    value = ', '.join(str(value))
                yield value

        return list(_generator())

    class Meta:
        abstract = True


class EventSurveyResult(SurveyResult):
    survey = models.ForeignKey('surveys.EventSurvey', on_delete=models.CASCADE)

    @property
    def event(self):
        return self.survey.event if self.survey else None

    def admin_get_event(self):
        return self.event
    admin_get_event.admin_order_field = 'survey__event'
    admin_get_event.short_description = _('Event')


class GlobalSurveyResult(SurveyResult):
    survey = models.ForeignKey('surveys.GlobalSurvey', on_delete=models.CASCADE)

    event = None
