from django.urls import re_path

from .views import listings_api_view, listings_listing_view

urlpatterns = [
    re_path(
        r"^listings/(?P<listing_hostname>[a-z0-9-\.]+)/?$",
        listings_listing_view,
        name="listings_listing_view",
    ),
    re_path(
        r"^api/v1/listings/(?P<listing_hostname>[a-z0-9-\.]+)/?$",
        listings_api_view,
        name="listings_api_view",
    ),
]
