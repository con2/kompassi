from __future__ import annotations

from typing import TYPE_CHECKING

from django.db import models, transaction
from django.utils.translation import gettext_lazy as _

from core.models import Event
from core.utils import NONUNIQUE_SLUG_FIELD_PARAMS, omit_keys, pick_attrs, slugify

from .personnel_class import PersonnelClass
from .qualifications import Qualification

if TYPE_CHECKING:
    from .roster import Job
    from .signup import Signup


def format_job_categories(job_categories):
    return ", ".join(jc.name for jc in job_categories)


class JobCategory(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, verbose_name=_("event"))
    app_label = models.CharField(max_length=63, blank=True, default="labour")

    # TODO rename this to "title"
    name = models.CharField(max_length=63, verbose_name=_("Name"))
    slug = models.CharField(**NONUNIQUE_SLUG_FIELD_PARAMS)  # type: ignore

    description = models.TextField(
        verbose_name=_("Description"),
        help_text=_(
            "This descriptions will be shown to the applicants on the signup form. If there are specific requirements to this job category, please mention them here."
        ),
        blank=True,
    )

    public = models.BooleanField(
        default=True,
        verbose_name=_("Publicly accepting applications"),
        help_text=_(
            "Job categories that are not accepting applications are not shown on the signup form. However, they may still be applied to using alternative signup forms."
        ),
    )

    required_qualifications = models.ManyToManyField(
        Qualification,
        blank=True,
        verbose_name=_("Required qualifications"),
    )

    personnel_classes = models.ManyToManyField(
        PersonnelClass,
        blank=True,
        verbose_name=_("Personnel classes"),
        help_text=_(
            "For most job categories, you should select the 'worker' and 'underofficer' classes here, if applicable."
        ),
    )

    accepted_signups: models.QuerySet[Signup]
    jobs: models.QuerySet[Job]

    @classmethod
    def get_or_create_dummy(
        cls,
        event: Event | None = None,
        personnel_class: PersonnelClass | None = None,
        name="Courier",
    ):
        from .labour_event_meta import LabourEventMeta

        if event is None:
            meta, _ = LabourEventMeta.get_or_create_dummy()
            event = meta.event
        else:
            meta, _ = LabourEventMeta.get_or_create_dummy(event=event)

        job_category, created = cls.objects.get_or_create(
            event=event,
            name=name,
        )

        if created:
            if personnel_class is None:
                personnel_class, _ = PersonnelClass.get_or_create_dummy(app_label="labour")

            job_category.personnel_classes.add(personnel_class)

        meta.create_groups()

        return job_category, created

    @classmethod
    def copy_from_event(cls, source_event, target_event, remap_personnel_classes=None):
        from .personnel_class import PersonnelClass

        if remap_personnel_classes is None:
            remap_personnel_classes = {}
        with transaction.atomic():
            for job_category in JobCategory.objects.filter(event=source_event):
                new_job_category, created = cls.objects.get_or_create(
                    event=target_event,
                    slug=job_category.slug,
                    defaults=omit_keys(vars(job_category), "_state", "id", "event_id", "slug"),
                )

                if not created:
                    continue

                for personnel_class in job_category.personnel_classes.all():
                    personnel_class_slug = remap_personnel_classes.get(
                        personnel_class.slug,
                        personnel_class.slug,
                    )

                    new_personnel_class, unused = PersonnelClass.objects.get_or_create(
                        event=target_event,
                        slug=personnel_class_slug,
                        defaults=omit_keys(vars(personnel_class), "_state", "id", "event_id", "slug"),
                    )
                    new_job_category.personnel_classes.add(new_personnel_class)

                for required_qualification in job_category.required_qualifications.all():
                    new_job_category.required_qualifications.add(required_qualification)

    @property
    def group(self):
        from django.contrib.auth.models import Group

        return Group.objects.get(name=self.event.labour_event_meta.make_group_name(self.event, self.slug))

    def is_person_qualified(self, person):
        if not self.required_qualifications.exists():
            return True

        else:
            quals = [pq.qualification for pq in person.qualifications.all()]
            return all(qual in quals for qual in self.required_qualifications.all())

    class Meta:
        verbose_name = _("job category")
        verbose_name_plural = _("job categories")
        ordering = ("event", "name")

        unique_together = [
            ("event", "slug"),
        ]

    def __str__(self):
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
        jc1, unused = cls.objects.get_or_create(event=event, name="Dummy 1", slug="dummy-1")
        jc2, unused = cls.objects.get_or_create(event=event, name="Dummy 2", slug="dummy-2")

        return [jc1, jc2]

    def _make_requirements(self):
        """
        Returns an array of integers representing the sum of JobRequirements for this JobCategory
        where indexes correspond to those of work_hours for this event.
        """
        from .roster import JobRequirement

        requirements = JobRequirement.objects.filter(job__job_category=self)
        return JobRequirement.requirements_as_integer_array(self.event, requirements)

    def _make_allocated(self):
        from .roster import JobRequirement, Shift

        shifts = Shift.objects.filter(job__job_category=self)
        return JobRequirement.allocated_as_integer_array(self.event, shifts)

    def _make_people(self):
        """
        Returns an array of accepted workers. Used by the Roster API.
        """
        return [
            signup.as_dict()
            for signup in (
                self.accepted_signups.filter(is_active=True)
                .order_by("person__surname", "person__first_name")
                .select_related("person")
            )
        ]

    def save(self, *args, **kwargs):
        if self.name and not self.slug:
            self.slug = slugify(self.name)

        return super().save(*args, **kwargs)

    def as_dict(self, include_jobs=False, include_requirements=False, include_people=False, include_shifts=False):
        if include_shifts and not include_jobs:
            raise AssertionError("If include_shifts is specified, must specify also include_jobs")

        doc = pick_attrs(
            self,
            "title",
            "slug",
        )

        if include_jobs:
            doc["jobs"] = [job.as_dict(include_shifts=include_shifts) for job in self.jobs.all()]

        if include_requirements:
            doc["requirements"] = self._make_requirements()
            doc["allocated"] = self._make_allocated()

        if include_people:
            doc["people"] = self._make_people()

        return doc

    def as_roster_api_dict(self):
        return self.as_dict(include_jobs=True, include_people=True, include_shifts=True)
