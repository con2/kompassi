# encoding: utf-8



from django.utils.translation import ugettext_lazy as _

from labour.views.labour_admin_startstop_view import generic_publish_unpublish_view

from ..proxies.programme_event_meta.cold_offers import ColdOffersProgrammeEventMetaProxy
from ..helpers import programme_admin_required
from ..forms import ColdOffersForm


@programme_admin_required
def programme_admin_cold_offers_view(request, vars, event):
    meta = ColdOffersProgrammeEventMetaProxy.objects.get(event=event)

    return generic_publish_unpublish_view(
        request, vars, event,
        meta=meta,
        template='programme_admin_cold_offers_view.pug',
        FormClass=ColdOffersForm,
        save_success_message=_("The times for cold offer period were saved."),
        start_now_success_message=_("The cold offer period was started."),
        stop_now_success_message=_("The cold offer period was ended."),
        already_public_message=_("The event was already accepting cold offers."),
    )
