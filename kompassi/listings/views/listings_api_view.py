from django.shortcuts import get_object_or_404

from kompassi.api.utils import api_view

from ..models import Listing


@api_view
def listings_api_view(request, listing_hostname):
    return get_object_or_404(Listing, hostname=listing_hostname).as_dict()
