from django.urls import reverse
from django.http import HttpResponseRedirect
from django.utils.http import urlencode


def url(view_name, *args):
    return reverse(view_name, args=args)


def login_redirect(request, view='core_login_view'):
    path = reverse(view)
    query = urlencode(dict(next=request.path))
    return HttpResponseRedirect("{path}?{query}".format(**locals()))


def get_next(request, default='/'):
    if request.method == 'GET':
        next = request.GET.get('next', None)
    elif request.method == 'POST':
        next = request.POST.get('next', None)
    else:
        raise NotImplementedError(request.method)

    return next if next else default
