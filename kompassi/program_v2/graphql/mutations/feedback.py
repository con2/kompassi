import logging

import graphene
from django.http import HttpRequest

from kompassi.core.utils.misc_utils import get_ip
from kompassi.zombies.programme.models.programme import Programme
from kompassi.zombies.programme.models.programme_feedback import ProgrammeFeedback

from ...models.program import Program

logger = logging.getLogger(__name__)


class ProgramFeedbackInput(graphene.InputObjectType):
    event_slug = graphene.String(required=True)
    program_slug = graphene.String(required=True)
    feedback = graphene.String(required=True)
    kissa = graphene.String(required=True)


class CreateProgramFeedback(graphene.Mutation):
    class Arguments:
        input = graphene.NonNull(ProgramFeedbackInput)

    success = graphene.NonNull(graphene.Boolean)

    def mutate(self, info, input):
        if not any(i in input.kissa.lower() for i in ["kissa", "cat", "katt"]):
            logger.error(f"Invalid kissa: {input.kissa}")
            return CreateProgramFeedback(success=False)  # type: ignore

        request: HttpRequest = info.context
        program = Program.objects.get(event__slug=input.event_slug, slug=input.program_slug)

        # TODO: feedback saved in Programme V1 for now
        try:
            programme = Programme.objects.get(category__event=program.event, slug=program.slug)
        except Programme.DoesNotExist:
            logger.error(f"Programme {program.slug} not found in V1")
            return CreateProgramFeedback(success=False)  # type: ignore

        is_own_programme = request.user.is_authenticated and request.user.person in programme.organizers.all()  # type: ignore

        ProgrammeFeedback.objects.create(
            programme=programme,
            feedback=input.feedback,
            author=request.user.person if request.user.is_authenticated else None,  # type: ignore
            is_anonymous=not request.user.is_authenticated or not is_own_programme,
            author_ip_address=get_ip(request),
        )

        return CreateProgramFeedback(success=True)  # type: ignore
