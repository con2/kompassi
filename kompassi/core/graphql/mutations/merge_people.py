import graphene
from django.http import HttpRequest
from graphql import GraphQLError

from kompassi.access.cbac import graphql_check_admin
from kompassi.core.merge_people import MergeConflictError, merge_people
from kompassi.graphql_api.errors import MERGE_CONFLICT

from ..admin import resolve_merge_plan
from ..person_admin import AdminPersonType


class MergePeopleInput(graphene.InputObjectType):
    into_person_id = graphene.Int(required=True)
    merge_person_ids = graphene.NonNull(graphene.List(graphene.NonNull(graphene.Int)))


class MergePeople(graphene.Mutation):
    """
    Combines duplicate accounts of the same person into `intoPersonId`, moving everything
    that refers to the others onto it and deleting them. Refuses with MERGE_CONFLICT when
    any record of a duplicate would collide with the survivor's.
    """

    class Arguments:
        input = MergePeopleInput(required=True)

    person = graphene.Field(AdminPersonType)

    @staticmethod
    def mutate(root, info, input: MergePeopleInput):
        request: HttpRequest = info.context
        into_person_id: int = input.into_person_id  # type: ignore
        merge_person_ids: list[int] = input.merge_person_ids  # type: ignore

        graphql_check_admin(info, model="Person", operation="update")

        plan = resolve_merge_plan([into_person_id, *merge_person_ids], into_person_id)

        try:
            merge_people(plan.into, plan.mergees, request=request)
        except MergeConflictError as e:
            raise GraphQLError(str(e), extensions={"code": MERGE_CONFLICT}) from e

        return MergePeople(person=plan.into)  # type: ignore
