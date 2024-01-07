import graphene
from graphene_django import DjangoObjectType

from core.models import Person
from core.utils import normalize_whitespace
from forms.graphql.meta import FormsProfileMetaType
from forms.models.meta import FormsProfileMeta


class ProfileType(DjangoObjectType):
    class Meta:
        model = Person
        fields = ()

    @staticmethod
    def resolve_forms(person: Person, info):
        """
        Namespace for queries related to forms and the current user.
        """
        return FormsProfileMeta(person)

    forms = graphene.Field(
        graphene.NonNull(FormsProfileMetaType),
        description=normalize_whitespace(resolve_forms.__doc__ or ""),
    )
