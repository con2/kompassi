# encoding: utf-8

from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _

from core.utils import NONUNIQUE_SLUG_FIELD_PARAMS, slugify, pick_attrs


def format_job_categories(job_categories):
    return u", ".join(jc.name for jc in job_categories)


class JobCategory(models.Model):
    event = models.ForeignKey('core.Event', verbose_name=_("event"))
    app_label = models.CharField(max_length=63, blank=True, default='labour')

    # TODO rename this to "title"
    name = models.CharField(max_length=63, verbose_name=_("Name"))
    slug = models.CharField(**NONUNIQUE_SLUG_FIELD_PARAMS)

    description = models.TextField(
        verbose_name=_("Description"),
        help_text=_("This descriptions will be shown to the applicants on the signup form. If there are specific requirements to this job category, please mention them here."),
        blank=True
    )

    public = models.BooleanField(
        default=True,
        verbose_name=_("Publicly accepting applications"),
        help_text=_("Job categories that are not accepting applications are not shown on the signup form. However, they may still be applied to using alternative signup forms."),
    )

    required_qualifications = models.ManyToManyField('labour.Qualification',
        blank=True,
        verbose_name=_("Required qualifications"),
    )

    personnel_classes = models.ManyToManyField('labour.PersonnelClass',
        blank=True,
        verbose_name=_("Personnel classes"),
        help_text=_("For most job categories, you should select the 'worker' and 'underofficer' classes here, if applicable."),
    )

    @classmethod
    def get_or_create_dummy(cls, name=u'Courier'):
        from core.models import Event
        from .labour_event_meta import LabourEventMeta
        from .personnel_class import PersonnelClass

        meta, unused = LabourEventMeta.get_or_create_dummy()
        event = meta.event

        job_category, created = cls.objects.get_or_create(
            event=event,
            name=name,
        )

        if created:
            personnel_class, unused = PersonnelClass.get_or_create_dummy(app_label='labour')
            job_category.personnel_classes.add(personnel_class)

        meta.create_groups()

        return job_category, created

    def is_person_qualified(self, person):
        if not self.required_qualifications.exists():
            return True

        else:
            quals = [pq.qualification for pq in person.personqualification_set.all()]
            return all(qual in quals for qual in self.required_qualifications.all())

    class Meta:
        verbose_name = _("job category")
        verbose_name_plural = _("job categories")
        ordering = ('event', 'name')

        unique_together = [
            ('event', 'slug'),
        ]

    def __unicode__(self):
        return self.name

    @property
    def title(self):
        return self.name
    @title.setter
    def title(self, new_title):
        self.name = new_title

    @classmethod
    def get_or_create_dummies(cls):
        from core.models import Event
        event, unused = Event.get_or_create_dummy()
        jc1, unused = cls.objects.get_or_create(event=event, name="Dummy 1", slug='dummy-1')
        jc2, unused = cls.objects.get_or_create(event=event, name="Dummy 2", slug='dummy-2')

        return [jc1, jc2]

    def _make_requirements(self):
        """
        Returns an array of integers representing the sum of JobRequirements for this JobCategory
        where indexes correspond to those of work_hours for this event.
        """
        from .roster import JobRequirement
        requirements = JobRequirement.objects.filter(job__job_category=self)
        return JobRequirement.requirements_as_integer_array(self.event, requirements)

    def save(self, *args, **kwargs):
        if self.name and not self.slug:
            self.slug = slugify(self.name)

        return super(JobCategory, self).save(*args, **kwargs)

    def as_dict(self, include_jobs=False, include_requirements=False):
        doc = pick_attrs(self,
            'title',
            'slug',
        )

        if include_jobs:
            doc['jobs'] = [job.as_dict() for job in self.job_set.all()]

        if include_requirements:
            doc['requirements'] = self._make_requirements()

        return doc
