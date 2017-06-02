from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils.translation import ugettext_lazy as _

from core.csv_export import CsvExportMixin


class SurveyResult(CsvExportMixin, models.Model):
    # Subclasses must provide a `survey` field
    # survey = models.ForeignKey(...)

    created_at = models.DateTimeField(auto_now_add=True)

    model = JSONField()

    author = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True)
    author_ip_address = models.CharField(
        max_length=48,
        blank=True,
        default='',
        verbose_name=_('IP address'),
    )

    def get_csv_fields(self, event):
        assert event == self.event

        def _generator():
            for page in self.survey.model['pages']:
                for element in page['elements']:
                    yield (self.__class__, element['name'])

        return list(_generator())

    def get_csv_row(self, event, fields, m2m_mode='separate_columns'):
        assert event == self.event

        return [self.model.get(field_name) for (cls, field_name) in fields]

    class Meta:
        abstract = True


class EventSurveyResult(SurveyResult):
    survey = models.ForeignKey('surveys.EventSurvey')

    @property
    def event(self):
        return self.survey.event if self.survey else None

    def admin_get_event(self):
        return self.event
    admin_get_event.admin_order_field = 'survey__event'
    admin_get_event.short_description = _('Event')


class GlobalSurveyResult(SurveyResult):
    survey = models.ForeignKey('surveys.GlobalSurvey')
