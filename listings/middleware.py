from django.conf import settings


class ListingsMiddleware(object):
    def process_request(self, request):
        hostname = request.META['HTTP_HOST']

        if hostname in settings.KOMPASSI_LISTING_URLCONFS:
            request.urlconf = settings.KOMPASSI_LISTING_URLCONFS[hostname]

        return None
