import pydantic


class DimensionValueDTO(pydantic.BaseModel):
    slug: str
    title: dict[str, str]
    color: str = ""
    is_technical: bool = False
    is_subject_locked: bool = False
