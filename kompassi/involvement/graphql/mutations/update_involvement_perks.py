import graphene
from django.db import transaction
from django.http import HttpRequest
from graphene.types.generic import GenericScalar

from kompassi.access.cbac import graphql_check_instance
from kompassi.core.models.event import Event
from kompassi.dimensions.models.cached_annotations import validate_annotations
from kompassi.dimensions.models.dimension_value import DimensionValue
from kompassi.event_log_v2.utils.emit import emit

from ...models.involvement import Involvement
from ...perks import MANUAL_PERKS_OVERRIDE_SLUG, get_perk_keys
from ..involvement_limited import LimitedInvolvementType


class UpdateInvolvementPerksInput(graphene.InputObjectType):
    event_slug = graphene.String(required=True)
    involvement_id = graphene.String(required=True)
    form_data = GenericScalar(required=True)


class UpdateInvolvementPerks(graphene.Mutation):
    """
    Manually override the automatically computed perks of a person's COMBINED_PERKS
    involvement, then recompute the non-overridden perks.

    ``form_data`` is ``{ overrides: string[], dimensions: {slug: string[]}, annotations: {slug: value} }``
    where ``overrides`` is the set of ticked override keys (``d-<dimension>`` / ``a-<annotation>``),
    and ``dimensions``/``annotations`` carry the manually set values for the overridden perks.
    """

    class Arguments:
        input = UpdateInvolvementPerksInput(required=True)

    involvement = graphene.Field(LimitedInvolvementType)

    @transaction.atomic
    @staticmethod
    def mutate(
        _root,
        info,
        input: UpdateInvolvementPerksInput,
    ):
        request: HttpRequest = info.context
        form_data: dict = input.form_data or {}  # type: ignore

        # while involvement_id would suffice and event_slug is not strictly necessary,
        # we want to validate event_slug because the caller will use it in redirects
        event = Event.objects.get(slug=input.event_slug)
        universe = event.involvement_universe
        involvement = Involvement.objects.get(universe=universe, id=input.involvement_id)

        # Overriding perks edits both dimensions and annotations on the involvement;
        # reuse the "dimensions" field so existing involvement admins are not locked out.
        graphql_check_instance(
            involvement,  # type: ignore
            info,
            field="dimensions",
            operation="update",
            app=involvement.app.app_name,
        )

        perk_keys = get_perk_keys(universe)
        new_overrides = {ov for ov in (form_data.get("overrides") or []) if ov in perk_keys}
        prev_overrides = set(involvement.cached_dimensions.get(MANUAL_PERKS_OVERRIDE_SLUG, []))
        cleared_overrides = prev_overrides - new_overrides

        submitted_dimensions: dict = form_data.get("dimensions") or {}
        submitted_annotations: dict = form_data.get("annotations") or {}

        # --- Dimension perks ---
        dimension_values_to_set: dict[str, list[str]] = {}
        # Cleared dimension perks are reset so the recompute restores the automatic value
        # (or leaves them empty if the Emperkelator does not compute them).
        for override_value in cleared_overrides:
            perk_key = perk_keys.get(override_value)
            if perk_key and perk_key.kind == "dimension":
                dimension_values_to_set[perk_key.slug] = []
        # Overridden dimension perks take the submitted value.
        for override_value in new_overrides:
            perk_key = perk_keys[override_value]
            if perk_key.kind == "dimension":
                value = submitted_dimensions.get(perk_key.slug, [])
                dimension_values_to_set[perk_key.slug] = value if isinstance(value, list) else [value]

        # Create the manual-perks-override values on demand (the dimension is technical and hidden).
        override_dimension = universe.dimensions.get(slug=MANUAL_PERKS_OVERRIDE_SLUG)
        for override_value in new_overrides:
            DimensionValue.objects.get_or_create(
                dimension=override_dimension,
                slug=override_value,
                defaults=dict(title_en=override_value, is_technical=True),
            )
        dimension_values_to_set[MANUAL_PERKS_OVERRIDE_SLUG] = sorted(new_overrides)

        cache = universe.preload_dimensions(dimension_slugs=dimension_values_to_set.keys())
        involvement.set_dimension_values(dimension_values_to_set, cache=cache)
        involvement.refresh_cached_dimensions()

        # --- Annotation perks ---
        annotations = dict(involvement.annotations)
        for override_value in cleared_overrides:
            perk_key = perk_keys.get(override_value)
            if perk_key and perk_key.kind == "annotation":
                annotations.pop(perk_key.slug, None)
        annotation_overrides = {
            perk_key.slug: submitted_annotations[perk_key.slug]
            for override_value in new_overrides
            if (perk_key := perk_keys[override_value]).kind == "annotation" and perk_key.slug in submitted_annotations
        }
        if annotation_overrides:
            # Validate against the schema, but store the raw submitted values.
            validate_annotations(annotation_overrides, universe.annotations.all())
            annotations.update(annotation_overrides)
        involvement.annotations = annotations
        involvement.save(update_fields=["annotations"])

        # Recompute non-overridden perks; _preserve_manual_perk_overrides keeps the overrides.
        recomputed = Involvement.for_combined_perks(event, involvement.person)

        emit(
            "involvement.perks.overridden",
            event=event,
            person=involvement.person,
            request=request,
            context=involvement.admin_link,
            other_fields=dict(perks_overridden=", ".join(sorted(new_overrides)) or "none"),
        )

        return UpdateInvolvementPerks(involvement=recomputed or involvement)  # type: ignore
