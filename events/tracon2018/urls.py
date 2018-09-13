from django.conf.urls import url

from .views import tracon2018_afterparty_participants_view, tracon2018_afterparty_summary_view


urlpatterns = [
    url(
        r'^events/(?P<event_slug>tracon2018)/labour/surveys/kaatoilmo/results.xlsx$',
        tracon2018_afterparty_participants_view,
        name='tracon2018_afterparty_participants_view',
    ),

    url(
        r'^events/(?P<event_slug>tracon2018)/labour/surveys/kaatoilmo/summary/?$',
        tracon2018_afterparty_summary_view,
        name='tracon2018_afterparty_participants_view',
    ),
]
