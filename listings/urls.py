from .views import listings_listing_view, listings_api_view
from django.urls import re_path


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
