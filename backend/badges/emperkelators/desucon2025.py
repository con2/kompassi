from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING, Self

import pydantic

from badges.models.survey_to_badge import SurveyToBadgeMapping
from badges.utils.default_badge_factory import default_badge_factory
from core.models.event import Event
from core.models.person import Person
from events.desucon2025.models import SHIRT_SIZES
from labour.models.personnel_class import PersonnelClass
from labour.models.signup import Signup

if TYPE_CHECKING:
    from ..models.badge import Badge


class ShirtMethod(str, Enum):
    DEFAULT = "DEFAULT"
    JOB_CATEGORY = "JOB_CATEGORY"
    JOB_TITLE = "JOB_TITLE"
    PROGRAM = "PROGRAM"


class ShirtType(Enum):
    NO_SHIRT = "NO_SHIRT", "Ei paitaa"
    TOO_LATE = "TOO_LATE", "Myöhästyi paitatilauksesta"
    STAFF = "STAFF", "Staff"
    KUVAAJA = "KUVAAJA", "Kuvaaja"
    DESURITY = "DESURITY", "Desurity"
    DESUTV = "DESUTV", "DesuTV"

    label: str

    def __new__(cls, value: str, label: str):
        obj = object.__new__(cls)
        obj._value_ = value
        obj.label = label
        return obj


# Set to True to freeze shirts (other perks still emperkelate normally)
SHIRT_DEADLINE_PASSED = False

SHIRT_SIZE_BY_SLUG: dict[str, str] = dict(SHIRT_SIZES)

# NOTE do not use for those who get badges via STB (generally you should use this only for organizers)
JOB_TITLE_MAPPING = {
    "Valokuvaus, Kompassi ja Tampere-logistiikka": ShirtType.KUVAAJA,  # that's me!
    "Yövastaava": ShirtType.DESURITY,
    "DesuTV- Vastaava": ShirtType.DESUTV,
    "Turvallisuusvastaava": ShirtType.DESURITY,
    "Turvallisuusvastaava II": ShirtType.DESURITY,
}

JOB_CATEGORY_MAPPING = {
    "DesuTV": ShirtType.DESUTV,
    "Järjestyksenvalvoja": ShirtType.DESURITY,
    "Valokuvaus": ShirtType.KUVAAJA,
}


class DesumPerkelator(pydantic.BaseModel):
    override_formatted_perks: str = ""
    shirt_size: str = "Ei paitaa"
    shirt_type: str = "Ei paitaa"
    shirt_method: ShirtMethod = ShirtMethod.DEFAULT

    def __str__(self):
        return self.override_formatted_perks

    @classmethod
    def emperkelate(
        cls,
        event: Event,
        person: Person,
        existing_badge: Badge | None = None,
    ) -> Self:
        badge_opts = default_badge_factory(event, person)
        personnel_class: PersonnelClass | None = badge_opts.get("personnel_class")  # type: ignore
        if not personnel_class:
            return cls()

        override_formatted_perks = personnel_class.override_formatted_perks
        job_title: str = badge_opts.get("job_title", "")
        shirt_method = ShirtMethod.DEFAULT
        shirt_type = ShirtType.STAFF
        shirt_size = "NO_SHIRT"

        # HACK: We know in Desucon Signups (kuutit) confer at least the same or better perks than STB (ohjelma)
        # So we do not consider STB perks if we have a Signup
        if signup := Signup.objects.filter(event=event, person=person).first():
            shirt_size = signup.signup_extra.shirt_size  # type: ignore
            if signup.override_formatted_perks:
                override_formatted_perks = signup.override_formatted_perks

            if badge_shirt_type := JOB_TITLE_MAPPING.get(job_title):
                shirt_type = badge_shirt_type
                shirt_method = ShirtMethod.JOB_TITLE
            else:
                for jc_name, jc_shirt_type in JOB_CATEGORY_MAPPING.items():
                    if signup.job_categories_accepted.filter(name=jc_name).exists():
                        shirt_type = jc_shirt_type
                        shirt_method = ShirtMethod.JOB_CATEGORY
                        break
        else:
            for mapping in (
                SurveyToBadgeMapping.objects.filter(survey__event=event)
                .select_related("personnel_class")
                .order_by("priority")
            ):
                if matches := mapping.match(person):
                    shirt_type = ShirtType.STAFF
                    shirt_method = ShirtMethod.PROGRAM
                    response, personnel_class, job_title = matches[0]
                    values, warnings = response.get_processed_form_data()
                    shirt_size = "NO_SHIRT" if "shirt_size" in warnings else values["shirt_size"]
                    override_formatted_perks = mapping.annotations.get("desucon2025:formattedPerks", "")
                    break

        shirt_size = shirt_size or "NO_SHIRT"
        shirt_size = SHIRT_SIZE_BY_SLUG[shirt_size]
        shirt_type = shirt_type.value

        if SHIRT_DEADLINE_PASSED:
            old_perks = cls.model_validate(existing_badge.perks) if existing_badge and existing_badge.perks else cls()
            shirt_size = old_perks.shirt_size
            shirt_type = old_perks.shirt_type
            shirt_method = old_perks.shirt_method

        return cls(
            override_formatted_perks=override_formatted_perks,
            shirt_size=shirt_size,
            shirt_type=shirt_type,
            shirt_method=shirt_method,
        )
