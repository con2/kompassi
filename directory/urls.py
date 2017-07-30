from django.conf.urls import include, url
from django.views.generic.base import RedirectView

from .views import directory_view


urlpatterns = [
    url(
        r'^organizations/(?P<organization_slug>[a-z0-9-]+)/directory/?$',
        directory_view,
        name='directory_view'
    ),
]
