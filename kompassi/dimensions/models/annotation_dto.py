from __future__ import annotations

from typing import ClassVar

from pydantic import BaseModel, Field

from .annotation import Annotation
from .enums import AnnotationAppliesTo, AnnotationDataType, AnnotationFlags


class AnnotationDTO(BaseModel, populate_by_name=True):
    """
    Legacy model from when Annotation schemas used to live in the code only.
    Now they have been migrated to the database, and this model is only used to
    bootstrap them.

    For everything else, use the `Annotation` model.
    """

    slug: str
    title: dict[str, str]
    description: dict[str, str] = Field(default_factory=dict)
    type: AnnotationDataType = Field(default=AnnotationDataType.STRING)

    is_applicable_to_program_items: bool = True
    is_applicable_to_schedule_items: bool = False
    is_applicable_to_involvements: bool = False

    is_public: bool = True
    is_shown_in_detail: bool = True
    is_computed: bool = False
    is_perk: bool = False

    def to_django(self) -> Annotation:
        return Annotation(
            slug=self.slug,
            # NOTE SUPPORTED_LANGUAGES
            title_fi=self.title.get("fi", ""),
            title_en=self.title.get("en", ""),
            title_sv=self.title.get("sv", ""),
            description_fi=self.description.get("fi", ""),
            description_en=self.description.get("en", ""),
            description_sv=self.description.get("sv", ""),
            type=self.type,
            applies_to=AnnotationAppliesTo.from_kwargs(
                is_applicable_to_program_items=self.is_applicable_to_program_items,
                is_applicable_to_schedule_items=self.is_applicable_to_schedule_items,
                is_applicable_to_involvements=self.is_applicable_to_involvements,
            ),
            flags=AnnotationFlags.from_kwargs(
                is_public=self.is_public,
                is_shown_in_detail=self.is_shown_in_detail,
                is_computed=self.is_computed,
                is_perk=self.is_perk,
            ),
        )

    def save(self) -> Annotation:
        return self.save_many([self])[0]

    update_fields: ClassVar[set[str]] = {
        # NOTE SUPPORTED_LANGUAGES
        "title_en",
        "title_fi",
        "title_sv",
        "description_en",
        "description_fi",
        "description_sv",
        "type",
        "applies_to",
        "flags",
    }

    @classmethod
    def save_many(cls, annotations: list[AnnotationDTO]) -> list[Annotation]:
        return Annotation.objects.bulk_create(
            [dto.to_django() for dto in annotations],
            unique_fields=["slug"],
            update_fields=cls.update_fields,
            update_conflicts=True,
        )
