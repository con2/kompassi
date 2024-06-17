from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class AnnotationDataType(Enum):
    STRING = "string"
    NUMBER = "number"
    BOOLEAN = "boolean"


class AnnotationSchemoid(BaseModel):
    slug: str
    title: dict[str, str]
    description: dict[str, str] = Field(default_factory=dict)
    type: AnnotationDataType = AnnotationDataType.STRING
    is_public: bool = True
    is_shown_in_detail: bool = True


class ProgramAnnotation(BaseModel):
    annotation: AnnotationSchemoid
    value: Any
