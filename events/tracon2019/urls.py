from django.conf.urls import url

from .views import tracon2019_afterparty_participants_view, tracon2019_afterparty_summary_view


urlpatterns = [
    url(
        r'^events/(?P<event_slug>tracon2019)/labour/surveys/kaatoilmo/results.xlsx$',
        tracon2019_afterparty_participants_view,
        name='tracon2019_afterparty_participants_view',
    ),

    url(
        r'^events/(?P<event_slug>tracon2019)/labour/surveys/kaatoilmo/summary/?$',
        tracon2019_afterparty_summary_view,
        name='tracon2019_afterparty_participants_view',
    ),
]
