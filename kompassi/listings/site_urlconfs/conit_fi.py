from django.urls import path

from ..views import listings_listing_view

handler403 = "access.views.error_views.permission_denied_view"
handler404 = "access.views.error_views.not_found_view"


urlpatterns = [
    path(
        "",
        listings_listing_view,
        dict(listing_hostname="conit.fi"),
        name="listings_listing_view",
    ),
]
