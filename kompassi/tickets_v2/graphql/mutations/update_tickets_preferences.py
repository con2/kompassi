import graphene
from django.core.exceptions import ValidationError

from kompassi.access.cbac import graphql_check_instance
from kompassi.core.models.contact_email_mixin import contact_email_validator

from ...models.meta import TicketsV2EventMeta
from ..meta import TicketsV2EventMetaType


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

        contact_email = (input.contact_email or "").strip()  # type: ignore
        if contact_email:
            try:
                contact_email_validator(contact_email)
            except ValidationError as e:
                raise ValueError("Invalid contact email (expected format: Name <email@example.com>)") from e

        cancellation_period_days: int = input.cancellation_period_days or 0  # type: ignore
        if cancellation_period_days < 0:
            raise ValueError("Cancellation period cannot be negative")

        meta.contact_email = contact_email
        meta.terms_and_conditions_url_en = input.terms_and_conditions_url_en or ""  # type: ignore
        meta.terms_and_conditions_url_fi = input.terms_and_conditions_url_fi or ""  # type: ignore
        meta.terms_and_conditions_url_sv = input.terms_and_conditions_url_sv or ""  # type: ignore
        meta.cancellation_period_days = cancellation_period_days
        meta.save(
            update_fields=[
                "contact_email",
                "terms_and_conditions_url_en",
                "terms_and_conditions_url_fi",
                "terms_and_conditions_url_sv",
                "cancellation_period_days",
            ]
        )

        return UpdateTicketsPreferences(preferences=meta)  # type: ignore
