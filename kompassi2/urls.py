from django.conf.urls import url
from graphene_django.views import GraphQLView

from csp.decorators import csp_exempt

urlpatterns = [
    url(r'^graphql', csp_exempt(GraphQLView.as_view(graphiql=True))),
]
