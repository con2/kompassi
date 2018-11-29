from django.contrib import messages
from django.contrib.postgres.search import SearchVector
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.utils.translation import ugettext_lazy as _

from core.sort_and_filter import Filter
from event_log.utils import emit

from ..forms import SearchForm
from ..helpers import directory_access_required


HIDE_WARNING_SESSION_KEY = 'directory.directory_view.hide_warning'


@directory_access_required
@require_http_methods(['GET', 'HEAD', 'POST'])
def directory_view(request, vars, organization):
    people = organization.people
    num_total_people = people.count()

    events = organization.events.all()
    event_filters = Filter(request, 'event').add_objects('event', events)
    event_slug = event_filters.selected_slug
    if event_slug:
        event = get_object_or_404(events, slug=event_slug)
        people = event.people
    else:
        event = None

    search_form = SearchForm(request.GET)
    if search_form.is_valid():
        query = search_form.cleaned_data['query']
        if query:
            people = people.annotate(
                search=SearchVector('first_name', 'surname', 'nick', 'email', 'phone', 'user__username'),
            ).filter(search=query)

    hide_warning = None
    if request.method == 'POST':
        if request.POST.get('action') == 'hide-warning':
            hide_warning = request.session[HIDE_WARNING_SESSION_KEY] = True
        else:
            messages.error(request, _('Unknown action.'))

    if hide_warning is None:
        hide_warning = request.session.get(HIDE_WARNING_SESSION_KEY, False)

    vars.update(
        event_filters=event_filters,
        num_total_people=num_total_people,
        people=people,
        search_form=search_form,
        show_warning=not hide_warning,
    )

    if search_form.is_valid() and query:
        emit('directory.search.performed', search_term=query, request=request, organization=organization)
    else:
        emit('directory.viewed', request=request, organization=organization)

    return render(request, 'directory_view.pug', vars)
