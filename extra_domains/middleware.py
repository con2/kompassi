from django.utils.cache import patch_vary_headers  

from .models import ExtraDomain


class ExtraDomainsMiddleware(object):
    def process_request(self, request):
        extra_domain = ExtraDomain.get_for_request(request)
        if not extra_domain:
            return

        request.urlconf = extra_domain.root_urlconf

    def process_view(self, request, view_func, view_args, view_kwargs):
        extra_domain = ExtraDomain.get_for_request(request)
        if not extra_domain:
            return

        view_args[0:0] = extra_domain.args
        for key, value in extra_domain.kwargs.iteritems():
            view_kwargs.setdefault(key, value)

    def process_response(self, request, response):  
        if getattr(request, "urlconf", None):  
            patch_vary_headers(response, ('Host',))  
        return response  