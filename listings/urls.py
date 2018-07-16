from django.conf.urls import url

from .views import listings_listing_view


urlpatterns = [
    url(
        r'^listings/(?P<listing_hostname>[a-z0-9-\.]+)/?$',
        listings_listing_view,
        name='listings_listing_view',
    ),
]
