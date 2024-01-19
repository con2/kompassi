import graphene


class DimensionFilterInput(graphene.InputObjectType):
    dimension = graphene.String()
    values = graphene.List(graphene.String)
