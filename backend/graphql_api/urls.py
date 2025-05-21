from csp.decorators import csp_exempt
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView

from .schema import schema

urlpatterns = [
    # TODO csp_exempt, csrf_exempt
    path("graphql", csp_exempt()(csrf_exempt(GraphQLView.as_view(graphiql=True, schema=schema)))),
]
