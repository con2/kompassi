from django.conf.urls import url

from .views import traconpaidat2019_custom_shirts_view


urlpatterns = [
    url(
        r'^events/(?P<event_slug>traconpaidat2019)/tickets/admin/customshirts.xlsx$',
        traconpaidat2019_custom_shirts_view,
        name='traconpaidat2019_custom_shirts_view',
    ),
]
