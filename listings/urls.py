from django.conf.urls import url

from .views import listings_listing_view, listings_api_view


urlpatterns = [
    url(
        r'^listings/(?P<listing_hostname>[a-z0-9-\.]+)/?$',
        listings_listing_view,
        name='listings_listing_view',
    ),

    url(
        r'^api/v1/listings/(?P<listing_hostname>[a-z0-9-\.]+)/?$',
        listings_api_view,
        name='listings_api_view',
    )
]
