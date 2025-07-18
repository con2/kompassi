import graphene

from core.graphql.event_full import FullEventType
from core.graphql.mutations.confirm_email import ConfirmEmail
from core.graphql.profile_own import OwnProfileType
from core.models import Event, Person
from core.utils import normalize_whitespace
from dimensions.graphql.mutations.delete_dimension import DeleteDimension
from dimensions.graphql.mutations.delete_dimension_value import DeleteDimensionValue
from dimensions.graphql.mutations.put_dimension import PutDimension
from dimensions.graphql.mutations.put_dimension_value import PutDimensionValue
from forms.graphql.mutations.create_survey import CreateSurvey
from forms.graphql.mutations.create_survey_language import CreateSurveyLanguage
from forms.graphql.mutations.create_survey_response import CreateSurveyResponse
from forms.graphql.mutations.delete_survey import DeleteSurvey
from forms.graphql.mutations.delete_survey_language import DeleteSurveyLanguage
from forms.graphql.mutations.delete_survey_responses import DeleteSurveyResponses
from forms.graphql.mutations.generate_key_pair import GenerateKeyPair
from forms.graphql.mutations.init_file_upload import InitFileUpload
from forms.graphql.mutations.promote_field_to_dimension import PromoteFieldToDimension
from forms.graphql.mutations.revoke_key_pair import RevokeKeyPair
from forms.graphql.mutations.subscriptions import SubscribeToSurveyResponses, UnsubscribeFromSurveyResponses
from forms.graphql.mutations.update_form import UpdateForm
from forms.graphql.mutations.update_form_fields import UpdateFormFields
from forms.graphql.mutations.update_response_dimensions import UpdateResponseDimensions
from forms.graphql.mutations.update_survey import UpdateSurvey
from forms.graphql.mutations.update_survey_default_dimensions import UpdateSurveyDefaultDimensions
from involvement.graphql.mutations.accept_invitation import AcceptInvitation
from involvement.graphql.mutations.delete_invitation import DeleteInvitation
from involvement.graphql.mutations.resend_invitation import ResendInvitation
from involvement.graphql.mutations.update_involvement_dimensions import UpdateInvolvementDimensions
from involvement.graphql.registry_limited import LimitedRegistryType
from involvement.models.registry import Registry
from program_v2.graphql.mutations.accept_program_offer import AcceptProgramOffer
from program_v2.graphql.mutations.cancel_program import CancelProgram
from program_v2.graphql.mutations.cancel_program_offer import CancelProgramOffer
from program_v2.graphql.mutations.create_program import CreateProgram
from program_v2.graphql.mutations.create_program_form import CreateProgramForm
from program_v2.graphql.mutations.delete_program_host import DeleteProgramHost
from program_v2.graphql.mutations.delete_schedule_item import DeleteScheduleItem
from program_v2.graphql.mutations.favorites import (
    MarkProgramAsFavorite,
    MarkScheduleItemAsFavorite,
    UnmarkProgramAsFavorite,
    UnmarkScheduleItemAsFavorite,
)
from program_v2.graphql.mutations.feedback import CreateProgramFeedback
from program_v2.graphql.mutations.invite_program_host import InviteProgramHost
from program_v2.graphql.mutations.put_event_annotation import PutEventAnnotation
from program_v2.graphql.mutations.put_schedule_item import PutScheduleItem
from program_v2.graphql.mutations.restore_program import RestoreProgram
from program_v2.graphql.mutations.update_program import UpdateProgram
from program_v2.graphql.mutations.update_program_annotations import UpdateProgramAnnotations
from program_v2.graphql.mutations.update_program_dimensions import UpdateProgramDimensions
from program_v2.graphql.mutations.update_program_form import UpdateProgramForm
from tickets_v2.graphql.mutations.cancel_and_refund_order import CancelAndRefundOrder
from tickets_v2.graphql.mutations.cancel_own_unpaid_order import CancelOwnUnpaidOrder
from tickets_v2.graphql.mutations.create_order import CreateOrder
from tickets_v2.graphql.mutations.create_product import CreateProduct
from tickets_v2.graphql.mutations.create_quota import CreateQuota
from tickets_v2.graphql.mutations.delete_product import DeleteProduct
from tickets_v2.graphql.mutations.delete_quota import DeleteQuota
from tickets_v2.graphql.mutations.mark_order_as_paid import MarkOrderAsPaid
from tickets_v2.graphql.mutations.reorder_products import ReorderProducts
from tickets_v2.graphql.mutations.resend_order_confirmation import ResendOrderConfirmation
from tickets_v2.graphql.mutations.update_order import UpdateOrder
from tickets_v2.graphql.mutations.update_product import UpdateProduct
from tickets_v2.graphql.mutations.update_quota import UpdateQuota

from .language import DEFAULT_LANGUAGE, Language


class LanguageType(graphene.ObjectType):
    code = graphene.String()
    name = graphene.String(lang=graphene.String())

    @staticmethod
    def resolve_name(
        language: Language,
        info,
        lang: str = DEFAULT_LANGUAGE,
    ):
        if lang == "fi":
            return language.name_fi
        else:
            return language.name_en


class Query(graphene.ObjectType):
    @staticmethod
    def resolve_event(root, info, slug: str):
        return Event.objects.filter(slug=slug).first()

    event = graphene.Field(FullEventType, slug=graphene.String(required=True))

    @staticmethod
    def resolve_profile(root, info):
        if not info.context.user.is_authenticated:
            return None

        try:
            return info.context.user.person
        except Person.DoesNotExist:
            return None

    profile = graphene.Field(OwnProfileType)

    @staticmethod
    def resolve_user_registry(root, info):
        """
        Returns the registry that hosts the personal data of
        all users of Kompassi.
        """
        return Registry.get_user_registry()

    user_registry = graphene.NonNull(
        LimitedRegistryType,
        description=normalize_whitespace(resolve_user_registry.__doc__ or ""),
    )


class Mutation(graphene.ObjectType):
    # Core
    confirm_email = ConfirmEmail.Field()

    # Forms
    create_survey = CreateSurvey.Field()
    update_survey = UpdateSurvey.Field()
    delete_survey = DeleteSurvey.Field()
    update_survey_default_dimensions = UpdateSurveyDefaultDimensions.Field()

    create_survey_language = CreateSurveyLanguage.Field()
    update_form = UpdateForm.Field()
    update_form_fields = UpdateFormFields.Field()
    delete_survey_language = DeleteSurveyLanguage.Field()
    promote_field_to_dimension = PromoteFieldToDimension.Field()

    create_survey_response = CreateSurveyResponse.Field()
    update_response_dimensions = UpdateResponseDimensions.Field()
    delete_survey_responses = DeleteSurveyResponses.Field()

    init_file_upload = InitFileUpload.Field()

    generate_key_pair = GenerateKeyPair.Field()
    revoke_key_pair = RevokeKeyPair.Field()

    # Dimensions
    put_dimension = PutDimension.Field()
    delete_dimension = DeleteDimension.Field()

    put_dimension_value = PutDimensionValue.Field()
    delete_dimension_value = DeleteDimensionValue.Field()

    # Involvement
    accept_invitation = AcceptInvitation.Field()
    delete_invitation = DeleteInvitation.Field()
    resend_invitation = ResendInvitation.Field()

    update_involvement_dimensions = UpdateInvolvementDimensions.Field()

    # Program v2
    mark_program_as_favorite = MarkProgramAsFavorite.Field()
    unmark_program_as_favorite = UnmarkProgramAsFavorite.Field()
    mark_schedule_item_as_favorite = MarkScheduleItemAsFavorite.Field()
    unmark_schedule_item_as_favorite = UnmarkScheduleItemAsFavorite.Field()

    create_program_feedback = CreateProgramFeedback.Field()

    subscribe_to_survey_responses = SubscribeToSurveyResponses.Field()
    unsubscribe_from_survey_responses = UnsubscribeFromSurveyResponses.Field()

    create_program_form = CreateProgramForm.Field()
    update_program_form = UpdateProgramForm.Field()

    accept_program_offer = AcceptProgramOffer.Field()
    cancel_program_offer = CancelProgramOffer.Field()

    create_program = CreateProgram.Field()
    update_program = UpdateProgram.Field()
    update_program_annotations = UpdateProgramAnnotations.Field()
    update_program_dimensions = UpdateProgramDimensions.Field()
    cancel_program = CancelProgram.Field()
    restore_program = RestoreProgram.Field()

    invite_program_host = InviteProgramHost.Field()
    delete_program_host = DeleteProgramHost.Field()

    put_schedule_item = PutScheduleItem.Field()
    delete_schedule_item = DeleteScheduleItem.Field()

    put_event_annotation = PutEventAnnotation.Field()

    # Tickets v2
    create_product = CreateProduct.Field()
    update_product = UpdateProduct.Field()
    delete_product = DeleteProduct.Field()
    reorder_products = ReorderProducts.Field()

    create_quota = CreateQuota.Field()
    update_quota = UpdateQuota.Field()
    delete_quota = DeleteQuota.Field()

    create_order = CreateOrder.Field()
    update_order = UpdateOrder.Field()
    resend_order_confirmation = ResendOrderConfirmation.Field()
    cancel_and_refund_order = CancelAndRefundOrder.Field()
    cancel_own_unpaid_order = CancelOwnUnpaidOrder.Field()
    mark_order_as_paid = MarkOrderAsPaid.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
