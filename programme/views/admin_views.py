from django.shortcuts import get_object_or_404, render

from core.utils import initialize_form, url

from ..models import Programme
from ..helpers import programme_admin_required
from ..forms import ProgrammeForm, ProgrammeAdminForm


@programme_admin_required
def programme_admin_view(request, vars, event):
    programmes = Programme.objects.filter(category__event=event)

    vars.update(
        programmes=programmes
    )

    return render(request, 'programme_admin_view.jade', vars)


@programme_admin_required
def programme_admin_detail_view(request, vars, event, programme_id):
    programme = get_object_or_404(Programme, category__event=event, pk=int(programme_id))

    programme_form = initialize_form(ProgrammeForm, request,
        instance=programme,
        prefix='programme_basic',
    )
    programme_admin_form = initialize_form(ProgrammeAdminForm, request,
        instance=programme,
        prefix='programme_admin',
    )

    vars.update(
        programme=programme,
        programme_form=programme_form,
        programme_admin_form=programme_admin_form,
    )

    return render(request, 'programme_admin_detail_view.jade', vars)


def programme_admin_menu_items(request, event):
    index_url = url('programme_admin_view', event.slug)
    index_active = request.path.startswith(index_url)
    index_text = u'Ohjelmaluettelo'

    return [
        (index_active, index_url, index_text),
    ]
