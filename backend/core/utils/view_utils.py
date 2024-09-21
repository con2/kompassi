from django.http import HttpRequest, HttpResponseRedirect
from django.urls import reverse
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


def get_event_and_organization(request: HttpRequest):
    from ..models.event import Event
    from ..models.organization import Organization

    event = None
    organization = None

    if resolver_match := request.resolver_match:
        if event_slug := resolver_match.kwargs.get("event_slug"):
            if event := Event.objects.filter(slug=event_slug).select_related("organization").first():
                organization = event.organization
        elif organization_slug := resolver_match.kwargs.get("organization_slug"):
            organization = Organization.objects.filter(slug=organization_slug).first()

    return event, organization
