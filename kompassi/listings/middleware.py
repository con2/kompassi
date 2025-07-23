from django.conf import settings
from django.utils.deprecation import MiddlewareMixin


class ListingsMiddleware(MiddlewareMixin):
    def process_request(self, request):
        hostname = request.headers.get("host", "")

        if hostname in settings.KOMPASSI_LISTING_URLCONFS:
            request.urlconf = settings.KOMPASSI_LISTING_URLCONFS[hostname]
