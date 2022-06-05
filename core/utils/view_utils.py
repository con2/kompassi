from django.urls import reverse
from django.http import HttpResponseRedirect
from django.utils.http import urlencode


def url(view_name, *args):
    return reverse(view_name, args=args)


def login_redirect(request, view="core_login_view"):
    path = reverse(view)
    query = urlencode(dict(next=request.path))
    return HttpResponseRedirect(f"{path}?{query}")


def get_next(request, default="/"):
    if request.method in ("POST", "PATCH", "PUT"):
        next = request.POST.get("next", None)
    else:
        next = request.GET.get("next", None)

    return next if next else default
