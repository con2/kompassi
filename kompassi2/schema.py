from graphene_django import DjangoObjectType
import graphene

from core.models import Event


class User(DjangoObjectType):
    class Meta:
        model = Event


class Query(graphene.ObjectType):
    events = graphene.List(Event)

    @graphene.resolve_only_args
    def resolve_events(self):
        return UserModel.objects.all()


schema = graphene.Schema(query=Query)
