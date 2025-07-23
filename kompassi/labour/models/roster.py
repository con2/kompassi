from __future__ import annotations

from collections import defaultdict, namedtuple
from datetime import timedelta

from dateutil.parser import parse as parse_date
from dateutil.tz import tzlocal
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from kompassi.api.utils import JSONSchemaObject
from kompassi.core.csv_export import CsvExportMixin
from kompassi.core.utils import NONUNIQUE_SLUG_FIELD_PARAMS, ONE_HOUR, format_interval, pick_attrs, slugify


class WorkPeriod(models.Model):
    event = models.ForeignKey("core.Event", on_delete=models.CASCADE, verbose_name=_("event"))

    description = models.CharField(
        max_length=63,
        verbose_name=_("description"),
    )

    start_time = models.DateTimeField(verbose_name=_("starting time"), blank=True, null=True)
    end_time = models.DateTimeField(verbose_name=_("ending time"), blank=True, null=True)

    class Meta:
        verbose_name = _("work period")
        verbose_name_plural = _("work periods")

    def __str__(self):
        return self.description


class Job(models.Model):
    id: int

    job_category = models.ForeignKey(
        "labour.JobCategory",
        on_delete=models.CASCADE,
        verbose_name=_("job category"),
        related_name="jobs",
    )
    slug = models.CharField(**NONUNIQUE_SLUG_FIELD_PARAMS)  # type: ignore
    title = models.CharField(max_length=63, verbose_name=_("job title"))

    shifts: models.QuerySet[Shift]
    requirements: models.QuerySet[JobRequirement]

    class Meta:
        verbose_name = _("job")
        verbose_name_plural = _("jobs")
        unique_together = [("job_category", "slug")]

    def save(self, *args, **kwargs):
        if self.title and not self.slug:
            self.slug = slugify(self.title)

        return super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def admin_get_event(self):
        return self.job_category.event if self.job_category else None

    admin_get_event.short_description = _("event")
    admin_get_event.admin_order_field = "job_category__event"

    def _make_requirements(self):
        """
        Returns an array of integers representing the sum of JobRequirements for this Job
        where indexes correspond to those of work_hours for this event.
        """
        return JobRequirement.requirements_as_integer_array(self.job_category.event, self.requirements.all())

    def _make_allocated(self):
        """
        Returns an array of integers representing the number of Shifts for this Job
        where indexes correspond to those of work_hours for this event.
        """
        return JobRequirement.allocated_as_integer_array(self.job_category.event, self.shifts.all())

    def _make_shifts(self):
        return [shift.as_dict() for shift in self.shifts.all()]

    def as_dict(self, include_requirements=True, include_shifts=False):
        doc = pick_attrs(
            self,
            "slug",
            "title",
        )

        if include_requirements:
            doc["requirements"] = self._make_requirements()
            doc["allocated"] = self._make_allocated()

        if include_shifts:
            doc["shifts"] = self._make_shifts()

        return doc


class JobRequirement(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, verbose_name=_("job"), related_name="requirements")

    count = models.IntegerField(verbose_name="vaadittu henkilömäärä", validators=[MinValueValidator(0)], default=0)

    start_time = models.DateTimeField(verbose_name=_("starting time"))
    end_time = models.DateTimeField(verbose_name=_("ending time"))

    @staticmethod
    def requirements_as_integer_array(event, requirements):
        work_hours = event.labour_event_meta.work_hours

        requirements_by_start_time = defaultdict(list)
        for requirement in requirements:
            requirements_by_start_time[requirement.start_time].append(requirement)

        return [sum(r.count for r in requirements_by_start_time[t]) for t in work_hours]

    @staticmethod
    def allocated_as_integer_array(event, shifts):
        work_hours = event.labour_event_meta.work_hours

        allocated_by_start_time = defaultdict(int)
        for shift in shifts:
            for start_time in shift.work_hours:
                allocated_by_start_time[start_time] += 1

        return [allocated_by_start_time[t] for t in work_hours]

    def save(self, *args, **kwargs):
        if self.start_time and not self.end_time:
            self.end_time = self.start_time + ONE_HOUR

        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = _("job requirement")
        verbose_name_plural = _("job requirements")


class Shift(models.Model, CsvExportMixin):
    id: int

    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="shifts")
    start_time = models.DateTimeField()
    hours = models.PositiveIntegerField()
    signup = models.ForeignKey("labour.Signup", on_delete=models.CASCADE, related_name="shifts")
    notes = models.TextField(blank=True)

    def as_dict(self):
        tz = tzlocal()

        return dict(
            id=self.id,
            job=self.job.id,
            startTime=self.start_time.astimezone(tz).isoformat() if self.start_time else None,
            hours=self.hours,
            person=self.signup.person.id if self.signup and self.signup.person else None,
            notes=self.notes,
            state="planned",  # TODO
        )

    @property
    def work_hours(self):
        cur_time = self.start_time
        for _i in range(self.hours):
            yield cur_time
            cur_time += ONE_HOUR

    @property
    def end_time(self):
        return self.start_time + timedelta(hours=self.hours)

    # https://github.com/pydata/pandas/issues/7056
    @property
    def start_time_local(self):
        return self.start_time.astimezone(tzlocal()).replace(tzinfo=None) if self.start_time else None

    @property
    def end_time_local(self):
        return self.end_time.astimezone(tzlocal()).replace(tzinfo=None) if self.end_time else None

    @property
    def formatted_duration(self):
        return f"{self.hours} h"

    def admin_get_event(self):
        return self.job.job_category.event if self.job and self.job.job_category else None

    admin_get_event.short_description = _("event")
    admin_get_event.admin_order_field = "job__job_category__event"

    def admin_get_job_category(self):
        return self.job.job_category if self.job else None

    admin_get_job_category.short_description = _("job category")
    admin_get_job_category.admin_order_field = "job__job_category"

    def admin_get_person(self):
        return self.signup.person if self.signup else None

    admin_get_person.short_description = _("person")
    admin_get_person.admin_order_field = "signup__person"

    @classmethod
    def get_csv_fields(cls, event):
        from kompassi.core.models import Person

        from ..models import Job, JobCategory

        return [
            (JobCategory, "name"),
            (Job, "title"),
            (Person, "surname"),
            (Person, "first_name"),
            (Person, "nick"),
            (Shift, "start_time_local"),
            (Shift, "end_time_local"),
            (Shift, "hours"),
        ]

    def get_csv_related(self):
        from kompassi.core.models import Person

        from ..models import Job, JobCategory

        return {
            JobCategory: self.job.job_category,
            Job: self.job,
            Person: self.signup.person,
        }

    def __str__(self):
        parts = [
            f"{format_interval(self.start_time, self.end_time)} ({self.hours} h): {self.job.job_category.title if self.job and self.job.job_category else None} ({self.job.title if self.job else None})"
        ]

        if self.notes:
            parts.append(self.notes)

        return "\n".join(parts)

    class Meta:
        verbose_name = _("shift")
        verbose_name_plural = _("shifts")
        ordering = ("job", "start_time")


SetJobRequirementsRequestBase = namedtuple("SetJobRequirementsRequest", "startTime hours required")


class SetJobRequirementsRequest(SetJobRequirementsRequestBase, JSONSchemaObject):
    schema = dict(
        type="object",
        properties=dict(
            startTime=dict(type="string", format="date-time"),
            hours=dict(type="integer", minimum=1, maximum=99),
            required=dict(type="integer", minimum=0, maximum=99),
        ),
        required=list(SetJobRequirementsRequestBase._fields),
    )


EditJobRequestBase = namedtuple("EditJobRequest", "title")


class EditJobRequest(EditJobRequestBase, JSONSchemaObject):
    schema = dict(
        type="object",
        properties=dict(
            title=dict(type="string", minLength=1),
        ),
        required=[
            "title",
        ],
    )


EditShiftRequestBase = namedtuple("EditShiftRequest", "job startTime hours person notes")


class EditShiftRequest(EditShiftRequestBase, JSONSchemaObject):
    schema = dict(
        type="object",
        properties=dict(
            hours=dict(type="integer", minimum=1, maximum=99),
            job=dict(type="string", minLength=1),
            notes=dict(type="string"),
            person=dict(type="integer", minimum=1),
            startTime=dict(type="string", format="date-time"),
        ),
        required=["job", "startTime", "person", "hours"],
    )

    def update(self, job_category, shift):
        from .signup import Signup

        shift.job = Job.objects.get(slug=self.job, job_category=job_category)
        shift.start_time = parse_date(self.startTime)
        shift.hours = self.hours
        shift.signup = Signup.objects.get(person=self.person, event=job_category.event)
        shift.notes = self.notes
