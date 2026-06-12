import graphene
from django.core.exceptions import ValidationError

from kompassi.access.cbac import graphql_check_instance
from kompassi.core.models.contact_email_mixin import contact_email_validator

from ...models.meta import TicketsV2EventMeta
from ..meta import TicketsV2EventMetaType

TEXT_FIELDS = [
    "contact_email",
    "terms_and_conditions_url_en",
    "terms_and_conditions_url_fi",
    "terms_and_conditions_url_sv",
]


class UpdateTicketsPreferencesInput(graphene.InputObjectType):
    event_slug = graphene.String(required=True)
    contact_email = graphene.String()
    terms_and_conditions_url_en = graphene.String()
    terms_and_conditions_url_fi = graphene.String()
    terms_and_conditions_url_sv = graphene.String()
    cancellation_period_days = graphene.Int()


class UpdateTicketsPreferences(graphene.Mutation):
    """
    Updates the tickets settings that are exposed to event admins.
    Fields omitted from the input are left unchanged (clear with an empty value).
    NOTE: provider_id is deliberately not settable here (super admin only).
    """

    class Arguments:
        input = UpdateTicketsPreferencesInput(required=True)

    preferences = graphene.Field(TicketsV2EventMetaType)

    @staticmethod
    def mutate(
        _root,
        info,
        input: UpdateTicketsPreferencesInput,
    ):
        meta = TicketsV2EventMeta.objects.get(event__slug=input.event_slug)

        graphql_check_instance(
            meta,
            info,
            app="tickets_v2",
            operation="update",
        )

        update_fields = []

        for field in TEXT_FIELDS:
            if (value := getattr(input, field)) is None:
                continue

            value = value.strip()

            if field == "contact_email" and value:
                try:
                    contact_email_validator(value)
                except ValidationError as e:
                    raise ValueError("Invalid contact email (expected format: Name <email@example.com>)") from e

            setattr(meta, field, value)
            update_fields.append(field)

        cancellation_period_days: int | None = input.cancellation_period_days  # type: ignore
        if cancellation_period_days is not None:
            if cancellation_period_days < 0:
                raise ValueError("Cancellation period cannot be negative")

            meta.cancellation_period_days = cancellation_period_days
            update_fields.append("cancellation_period_days")

        if update_fields:
            meta.save(update_fields=update_fields)

        return UpdateTicketsPreferences(preferences=meta)  # type: ignore
