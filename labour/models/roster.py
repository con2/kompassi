# encoding: utf-8

from collections import namedtuple, defaultdict

from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _

from api.utils import JSONSchemaObject
from core.utils import NONUNIQUE_SLUG_FIELD_PARAMS, slugify


class WorkPeriod(models.Model):
    event = models.ForeignKey('core.Event', verbose_name=u'Tapahtuma')

    description = models.CharField(
        max_length=63,
        verbose_name=u'Kuvaus'
    )

    start_time = models.DateTimeField(verbose_name=u'Alkuaika', blank=True, null=True)
    end_time = models.DateTimeField(verbose_name=u'Loppuaika', blank=True, null=True)

    class Meta:
        verbose_name = _(u'work period')
        verbose_name_plural= _(u'work periods')

    def __unicode__(self):
        return self.description


class Job(models.Model):
    job_category = models.ForeignKey('labour.JobCategory', verbose_name=u'tehtäväalue')
    slug = models.CharField(**NONUNIQUE_SLUG_FIELD_PARAMS)
    title = models.CharField(max_length=63, verbose_name=u'tehtävän nimi')

    class Meta:
        verbose_name = _(u'job')
        verbose_name_plural = _(u'jobs')
        unique_together = [('job_category', 'slug')]

    def save(self, *args, **kwargs):
        if self.title and not self.slug:
            self.slug = slugify(self.title)

        return super(Job, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.title

    def admin_get_event(self):
        return self.job_category.event if self.job_category else None
    admin_get_event.short_description = u'Tapahtuma'
    admin_get_event.admin_order_field = 'job_category__event'

    def _make_requirements(self):
        """
        Returns an array of integers representing the sum of JobRequirements for this JobCategory
        where indexes correspond to those of work_hours for this event.
        """
        return JobRequirement.requirements_as_integer_array(self.job_category.event, self.requirements.all())

    def as_dict(self):
        return pick_attrs(self,
            'slug',
            'title',
            requirements=self._make_requirements(),
        )


class JobRequirement(models.Model):
    job = models.ForeignKey(Job, verbose_name=u'tehtävä', related_name='requirements')

    count = models.IntegerField(
        verbose_name=u'vaadittu henkilömäärä',
        validators=[MinValueValidator(0)],
        default=0
    )

    start_time = models.DateTimeField(verbose_name=u'vaatimuksen alkuaika')
    end_time = models.DateTimeField(verbose_name=u'vaatimuksen päättymisaika')

    @staticmethod
    def requirements_as_integer_array(event, requirements):
        work_hours = event.labour_event_meta.work_hours

        requirements_by_start_time = defaultdict(list)
        for requirement in requirements:
            requirements_by_start_time[requirement.start_time].append(requirement)

        return [sum(r.count for r in requirements_by_start_time[t]) for t in work_hours]

    def save(self, *args, **kwargs):
        if self.start_time and not self.end_time:
            self.end_time = self.start_time + ONE_HOUR

        return super(JobRequirement, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _(u'job requirement')
        verbose_name_plural = _(u'job requirements')


SetJobRequirementsRequestBase = namedtuple('SetJobRequirementsRequest', 'startTime hours required')
class SetJobRequirementsRequest(SetJobRequirementsRequestBase, JSONSchemaObject):
    schema = dict(
        type='object',
        properties=dict(
            startTime=dict(type='string', format='date-time'),
            hours=dict(type='integer', minimum=1, maximum=99),
            required=dict(type='integer', minimum=0, maximum=99),
        ),
        required=list(SetJobRequirementsRequestBase._fields),
    )


EditJobRequestBase = namedtuple('EditJobRequest', 'title')
class EditJobRequest(EditJobRequestBase, JSONSchemaObject):
    schema = dict(
        type='object',
        properties=dict(
            title=dict(type='string', minLength=1),
        ),
        required=['title',],
    )
