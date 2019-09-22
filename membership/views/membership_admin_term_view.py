from datetime import date

from django.views.decorators.http import require_http_methods
from django.shortcuts import get_object_or_404, render, redirect
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages

from core.utils import initialize_form, url

from ..helpers import membership_admin_required
from ..models import Term
from ..forms import TermForm


class NewTerm:
    pk = None
    id = None
    title = 'Uusi'

    def __init__(self, organization):
        self.organization = organization

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return url('membership_admin_new_term_view', self.organization.slug)


@membership_admin_required
@require_http_methods(['GET', 'HEAD', 'POST'])
def membership_admin_term_view(request, vars, organization, term_id=None):
    meta = organization.membership_organization_meta

    if term_id:
        term = get_object_or_404(Term, id=int(term_id), organization=organization)
    else:
        term = Term(organization=organization)

    terms = [
        (the_term, (the_term.pk == term.pk if term else False))
        for the_term in Term.objects.filter(organization=organization)
    ]
    terms.append((NewTerm(organization), (term_id is None)))

    today = date.today()
    form = initialize_form(TermForm, request, instance=term, initial={} if term.pk else dict(
       title=today.year,
       start_date=today.replace(month=1, day=1),
       end_date=today.replace(month=12, day=31),
    ))

    if request.method == 'POST':
        if form.is_valid():
            term = form.save()
            return redirect('membership_admin_term_view', organization_slug=organization.slug, term_id=term.id)
        else:
            messages.error(request, _('Please check the form.'))

    vars.update(
        form=form,
        meta=meta,
        term=term,
        terms=terms,
    )

    return render(request, 'membership_admin_term_view.pug', vars)
