from urllib import urlencode

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect


def login_redirect(request):
    path = reverse('core_login_view')
    query = urlencode(dict(next=request.path))
    return HttpResponseRedirect("{path}?{query}".format(**locals()))
