from django.contrib.auth.models import AbstractBaseUser, AnonymousUser
from django.db import models
from django.http import QueryDict

from forms.utils.process_form_data import FALSY_VALUES

from .models.program import Program


def filter_program(
    programs: models.QuerySet[Program],
    filters: QueryDict | dict[str, list[str]],
    user: AbstractBaseUser | AnonymousUser | None = None,
):
    if isinstance(filters, QueryDict):
        filters = {k: [str(v) for v in vs] for k, vs in filters.lists()}

    # filter programs by slug (may be ?slug=a&slug=b or ?slug=a,b,c)
    slugs = [slug for slugs in filters.pop("slug", []) for slug in slugs.split(",")]
    if slugs:
        programs = programs.filter(slug__in=slugs)

    # filter programs by favorited status
    favorited = filters.pop("favorited", [])
    if any(v.lower() not in FALSY_VALUES for v in favorited):
        if user and user.is_authenticated:
            programs = programs.filter(favorited_by=user)
        else:
            programs = programs.none()

    # filter programs by dimensions
    # TODO encapsulate this logic in a helper function
    for dimension_slug, value_slugs in filters.items():
        value_slugs = [slug for slugs in value_slugs for slug in slugs.split(",")]
        programs = programs.filter(
            dimensions__dimension__slug=dimension_slug,
            dimensions__value__slug__in=value_slugs,
        )

    return programs
