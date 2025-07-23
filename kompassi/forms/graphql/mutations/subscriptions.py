import graphene

from kompassi.access.cbac import graphql_check_instance

from ...models.survey import Survey


class SubscriptionInput(graphene.InputObjectType):
    event_slug = graphene.String(required=True)
    survey_slug = graphene.String(required=True)


class SubscribeToSurveyResponses(graphene.Mutation):
    class Arguments:
        input = graphene.NonNull(SubscriptionInput)

    success = graphene.NonNull(graphene.Boolean)

    def mutate(self, info, input):
        survey = Survey.objects.get(event__slug=input.event_slug, slug=input.survey_slug)
        graphql_check_instance(survey, info, field="subscribers", operation="create")

        survey.subscribers.add(info.context.user)

        return SubscribeToSurveyResponses(success=True)  # type: ignore


class UnsubscribeFromSurveyResponses(graphene.Mutation):
    class Arguments:
        input = graphene.NonNull(SubscriptionInput)

    success = graphene.NonNull(graphene.Boolean)

    def mutate(self, info, input):
        survey = Survey.objects.get(event__slug=input.event_slug, slug=input.survey_slug)

        graphql_check_instance(
            survey,
            info,
            app=survey.app_name,
            field="subscribers",
            operation="delete",
        )

        survey.subscribers.remove(info.context.user)

        return UnsubscribeFromSurveyResponses(success=True)  # type: ignore
