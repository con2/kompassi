from __future__ import annotations

from collections import Counter

from kompassi.core.models.event import Event
from kompassi.dimensions.models.annotation_dto import AnnotationDTO
from kompassi.forms.models.survey import Survey
from kompassi.graphql_api.utils import get_message_in_language
from kompassi.labour.views.admin_special_diets_view import NO_SPECIAL_DIET_REPLIES
from kompassi.reports.graphql.report import Column, Report, TypeOfColumn
from kompassi.reports.models.report import COUNT_TITLE, TOTAL_TITLE

from ..models.enums import InvolvementType
from ..models.involvement import Involvement


def report_tracon_other_benefits(event: Event, annotation_dtos: list[AnnotationDTO], lang: str):
    """
    TODO Generalize this
    Use AnnotationFlags.PERK to filter and count all countable annotations (int or boolean)
    """
    annotationsies = list(
        Involvement.objects.filter(
            universe=event.involvement_universe,
            type=InvolvementType.COMBINED_PERKS,
            is_active=True,
        ).values_list("annotations", flat=True)
    )

    meal_vouchers_annotation_dto = next(dto for dto in annotation_dtos if dto.slug == "tracon:mealVouchers")
    meal_vouchers_title = get_message_in_language(meal_vouchers_annotation_dto.title, lang)
    total_meal_vouchers = sum(
        annotations.get("tracon:mealVouchers", 0) for annotations in annotationsies if isinstance(annotations, dict)
    )

    extra_swag_annotation_dto = next(dto for dto in annotation_dtos if dto.slug == "tracon:extraSwag")
    extra_swag_title = get_message_in_language(extra_swag_annotation_dto.title, lang)
    total_extra_swag = sum(
        annotations.get("tracon:extraSwag", False) for annotations in annotationsies if isinstance(annotations, dict)
    )

    return Report(
        slug="tracon_other_benefits",
        title=dict(
            fi="Tracon: Muut edut",
            en="Tracon: Other perks",
        ),
        columns=[
            Column(
                slug="perk",
                title=dict(
                    en="Perk",
                    fi="Etu",
                ),
                type=TypeOfColumn.STRING,
            ),
            Column(
                slug="count",
                title=dict(
                    en="Count",
                    fi="Lukumäärä",
                ),
                type=TypeOfColumn.INT,
            ),
        ],
        rows=[
            [extra_swag_title, total_extra_swag],
            [meal_vouchers_title, total_meal_vouchers],
        ],
    )


def normalize_special_diet(special_diet: frozenset[str]) -> frozenset[str]:
    for stricter, less_strict in [
        ("Vegaaninen", "Maidoton"),
        ("Vegaaninen", "Laktoositon"),
        ("Vegaaninen", "Lakto-ovo-vegetaristinen"),
        ("Maidoton", "Laktoositon"),
    ]:
        if stricter in special_diet and less_strict in special_diet:
            special_diet -= {less_strict}

    return special_diet


def normalize_special_diet_other(special_diet_other: str) -> str:
    if not special_diet_other:
        return ""

    special_diet_other = special_diet_other.strip()

    if special_diet_other in NO_SPECIAL_DIET_REPLIES:
        special_diet_other = ""

    return special_diet_other


NO_SPECIAL_DIET = dict(en="No special diet", fi="Ei erikoisruokavaliota")
OTHER_SPECIAL_DIET = dict(en="Other special diet (see other table)", fi="Muu erikoisruokavalio (ks. toinen taulukko)")


def report_tracon_special_diets(
    event: Event,
    lang: str,
    *,
    v2_form_slug: str = "programhost",
    v2_special_diet_field_name: str = "specialdiet",
    v2_special_diet_other_field_name: str = "specialdiet-other",
) -> list[Report]:
    involvement_meta = event.involvement_event_meta
    if involvement_meta is None:
        raise ValueError("No InvolvementEventMeta")

    special_diet_by_user_id: dict[int, frozenset[str]] = dict()
    special_diet_other_by_user_id: dict[int, str] = dict()
    user_ids: set[int] = set()

    # Labour v1
    labour_meta = event.labour_event_meta
    if labour_meta is not None:
        for signup_extra in (
            labour_meta.signup_extra_model.objects.filter(is_active=True)
            .select_related("person__user")
            .prefetch_related("special_diet")
        ):
            user_ids.add(signup_extra.person.user_id)

            v1_special_diet: frozenset[str] = frozenset(d.name for d in signup_extra.special_diet.all())
            if v1_special_diet:
                special_diet_by_user_id[signup_extra.person.user_id] = normalize_special_diet(v1_special_diet)

            if v1_normalized_special_diet_other := normalize_special_diet_other(signup_extra.special_diet_other):
                special_diet_other_by_user_id[signup_extra.person.user_id] = v1_normalized_special_diet_other

    # Program v2
    survey = Survey.objects.filter(event=event, slug=v2_form_slug).first()
    if survey is not None:
        special_diet_field = next(
            field
            for field in survey.languages.get(language="fi").validated_fields
            if field.slug == v2_special_diet_field_name
        )
        special_diet_mapping = {choice.slug: choice.title for choice in special_diet_field.choices or []}

        for response in survey.current_responses:
            if not response.original_created_by_id:
                raise ValueError("cannot be")

            user_ids.add(response.original_created_by_id)

            # TODO does not currently filter out program hosts who have since cancelled or been removed
            values, warnings = response.get_processed_form_data(
                field_slugs=[v2_special_diet_field_name, v2_special_diet_other_field_name]
            )
            if v2_special_diet_field_name not in warnings:
                special_diet_slugs: list[str] = values.get(v2_special_diet_field_name, [])
                v2_special_diet: frozenset[str] = frozenset(special_diet_mapping[slug] for slug in special_diet_slugs)

                if v2_special_diet:
                    special_diet_by_user_id[response.original_created_by_id] = normalize_special_diet(v2_special_diet)

            if (
                v2_special_diet_other_field_name not in warnings
                and (v2_special_diet_other := values.get(v2_special_diet_other_field_name, ""))
                and (v2_normalized_special_diet_other := normalize_special_diet_other(v2_special_diet_other))
            ):
                special_diet_other_by_user_id[response.original_created_by_id] = v2_normalized_special_diet_other

    special_diet_combinations: Counter[frozenset[str]] = Counter(
        special_diet
        for (person_id, special_diet) in special_diet_by_user_id.items()
        if person_id not in special_diet_other_by_user_id
    )

    num_users_without = sum(
        1
        for user_id in user_ids
        if user_id not in special_diet_by_user_id and user_id not in special_diet_other_by_user_id
    )

    return [
        Report(
            slug="tracon_special_diets",
            title=dict(
                fi="Tracon: Erikoisruokavaliot",
                en="Tracon: Special diets",
            ),
            columns=[
                Column(
                    slug="special_diet",
                    title=dict(
                        fi="Erikoisruokavalio",
                        en="Special diet",
                    ),
                    type=TypeOfColumn.STRING,
                ),
                Column(
                    slug="count",
                    title=COUNT_TITLE,
                    type=TypeOfColumn.INT,
                ),
            ],
            rows=[
                [NO_SPECIAL_DIET[lang], num_users_without],
                [OTHER_SPECIAL_DIET[lang], len(special_diet_other_by_user_id)],
                *(
                    [", ".join(special_diet).lower(), count]
                    for (special_diet, count) in sorted(special_diet_combinations.items(), key=lambda x: -x[1])
                ),
            ],
            total_row=[TOTAL_TITLE[lang], len(user_ids)],
        ),
        Report(
            slug="tracon_special_diet_other",
            title=dict(
                fi="Tracon: Muut erikoisruokavaliot",
                en="Tracon: Other special diets",
            ),
            columns=[
                Column(
                    slug="special_diet_other",
                    title=dict(
                        fi="Avoimeen kenttään syötetty erikoisruokavalio",
                        en="Special diet filled in free text field",
                    ),
                    type=TypeOfColumn.STRING,
                ),
                Column(
                    slug="special_diet",
                    title=dict(
                        fi="Ruksattu erikoisruokavalio",
                        en="Ticked special diet",
                    ),
                    type=TypeOfColumn.STRING,
                ),
            ],
            rows=[
                [
                    special_diet_other,
                    ", ".join(special_diet_by_user_id.get(person_id, [])).lower(),
                ]
                for (person_id, special_diet_other) in special_diet_other_by_user_id.items()
            ],
            total_row=[TOTAL_TITLE[lang], len(special_diet_other_by_user_id)],
        ),
    ]
