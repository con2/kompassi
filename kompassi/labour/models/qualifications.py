from __future__ import annotations

from django.db import models
from django.utils.translation import gettext_lazy as _

from kompassi.core.utils import SLUG_FIELD_PARAMS


class Qualification(models.Model):
    slug = models.CharField(**SLUG_FIELD_PARAMS)  # type: ignore

    name = models.CharField(max_length=63, verbose_name="pätevyyden nimi")
    description = models.TextField(blank=True, verbose_name="kuvaus")

    qualification_extra_content_type = models.ForeignKey(
        "contenttypes.ContentType", on_delete=models.CASCADE, null=True, blank=True
    )

    person_qualifications: models.QuerySet[PersonQualification]

    class Meta:
        verbose_name = _("qualification")
        verbose_name_plural = _("qualifications")

    def __str__(self):
        return self.name

    @property
    def qualification_extra_model(self):
        if self.qualification_extra_content_type:
            return self.qualification_extra_content_type.model_class()
        else:
            return None

    @classmethod
    def create_dummy(cls):
        return cls.objects.create(name="Dummy qualification")

    @classmethod
    def get_or_create_dummies(cls):
        qual1, unused = Qualification.objects.get_or_create(slug="dummy1", defaults=dict(name="Dummy qualification 1"))
        qual2, unused = Qualification.objects.get_or_create(slug="dummy2", defaults=dict(name="Dummy qualification 2"))
        return [qual1, qual2]


class PersonQualification(models.Model):
    person = models.ForeignKey(
        "core.Person",
        on_delete=models.CASCADE,
        verbose_name="henkilö",
        related_name="qualifications",
    )
    qualification = models.ForeignKey(
        Qualification,
        on_delete=models.CASCADE,
        verbose_name="pätevyys",
        related_name="person_qualifications",
    )

    class Meta:
        verbose_name = _("qualification holder")
        verbose_name_plural = _("qualification holders")

    def __str__(self):
        return self.qualification.name if self.qualification else "None"

    @property
    def qualification_extra(self):
        if not self.qualification:
            return None

        QualificationExtra = self.qualification.qualification_extra_model
        if not QualificationExtra:
            return None

        if self.pk:
            try:
                return QualificationExtra.objects.get(personqualification=self)
            except QualificationExtra.DoesNotExist:
                pass

        return QualificationExtra(personqualification=self)


class QualificationExtraBase(models.Model):
    personqualification = models.OneToOneField(
        PersonQualification, on_delete=models.CASCADE, related_name="+", primary_key=True
    )

    @classmethod
    def get_form_class(cls):
        raise NotImplementedError("Remember to override get_form_class in your QualificationExtra model")

    class Meta:
        abstract = True
