from django.conf.urls import url

from ..views import listings_listing_view


handler403 = 'access.views.permission_denied_view'
handler404 = 'access.views.not_found_view'


urlpatterns = [
    url(
        r'^$',
        listings_listing_view,
        dict(listing_hostname='conit.fi'),
        name='listings_listing_view',
    ),
]
