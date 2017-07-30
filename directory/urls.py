from django.conf.urls import url

from .views import directory_view, directory_person_view


urlpatterns = [
    url(
        r'^organizations/(?P<organization_slug>[a-z0-9-]+)/people/?$',
        directory_view,
        name='directory_view'
    ),

    url(
        r'^organizations/(?P<organization_slug>[a-z0-9-]+)/people/(?P<person_id>[0-9]+)/?$',
        directory_person_view,
        name='directory_person_view'
    ),
]
