from __future__ import annotations

from enum import Flag
from logging import getLogger
from typing import TYPE_CHECKING

from django.db import models
from django_enum import EnumField

from .enums import AnnotationAppliesTo, AnnotationDataType, AnnotationFlags

if TYPE_CHECKING:
    pass

logger = getLogger(__name__)


def flag_getter(field_name: str, member: Flag):
    def getter(self):
        return bool(getattr(self, field_name) & member)

    return property(getter)


class Annotation(models.Model):
    slug = models.SlugField(unique=True)

    # NOTE SUPPORTED_LANGUAGES
    title_en = models.TextField(blank=True, default="")
    title_fi = models.TextField(blank=True, default="")
    title_sv = models.TextField(blank=True, default="")

    description_en = models.TextField(blank=True, default="")
    description_fi = models.TextField(blank=True, default="")
    description_sv = models.TextField(blank=True, default="")

    type: AnnotationDataType = EnumField(AnnotationDataType)  # type: ignore

    applies_to: AnnotationAppliesTo = EnumField(
        AnnotationAppliesTo,
        default=AnnotationAppliesTo.PROGRAM_ITEM,
    )  # type: ignore
    is_applicable_to_program_items = flag_getter("applies_to", AnnotationAppliesTo.PROGRAM_ITEM)
    is_applicable_to_schedule_items = flag_getter("applies_to", AnnotationAppliesTo.SCHEDULE_ITEM)
    is_applicable_to_involvements = flag_getter("applies_to", AnnotationAppliesTo.INVOLVEMENT)

    flags: AnnotationFlags = EnumField(
        AnnotationFlags,
        default=AnnotationFlags.PUBLIC,
    )  # type: ignore
    is_public = flag_getter("flags", AnnotationFlags.PUBLIC)
    is_shown_in_detail = flag_getter("flags", AnnotationFlags.SHOWN_IN_DETAIL)
    is_computed = flag_getter("flags", AnnotationFlags.COMPUTED)
    is_perk = flag_getter("flags", AnnotationFlags.PERK)

    @property
    def is_internal(self) -> bool:
        return self.slug.startswith("internal:")

    def __str__(self):
        return self.slug
