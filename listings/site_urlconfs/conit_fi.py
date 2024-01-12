from ..views import listings_listing_view
from django.urls import path


handler403 = "access.views.permission_denied_view"
handler404 = "access.views.not_found_view"


urlpatterns = [
    path(
        "",
        listings_listing_view,
        dict(listing_hostname="conit.fi"),
        name="listings_listing_view",
    ),
]
