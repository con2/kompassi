from functools import wraps

from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse

from core.utils import horizontal_form_helper
from paikkala.views import (
    RelinquishView as BaseRelinquishView,
    ReservationView as BaseReservationView,
    InspectionView as BaseInspectionView,
)

from ..forms import ReservationForm
from ..helpers import programme_event_required
from ..models import Programme


class PaikkalAdapterMixin:
    """
    Translates between Kompassi and Paikkala.
    """
    def get_context_data(self, **kwargs):
        """
        Kompassi `base.pug` template needs `event`.
        """
        context = super().get_context_data(**kwargs)
        context['event'] = self.kwargs['event']
        return context

    def get_programme(self):
        event = self.kwargs['event']
        programme_id = self.kwargs['programme_id']  # NOTE: programme.Programme, not paikkala.Program
        return Programme.objects.get(
            id=int(programme_id),
            category__event=event,
            is_using_paikkala=True,
            paikkala_program__isnull=False,
        )

    def get_success_url(self):
        return reverse('programme_profile_reservations_view')


class InspectionView(PaikkalAdapterMixin, BaseInspectionView):
    template_name = 'paikkala_inspection_view.pug'


class RelinquishView(PaikkalAdapterMixin, BaseRelinquishView):
    success_message_template = _('Successfully relinquished the seat reservation.')


class ReservationView(PaikkalAdapterMixin, BaseReservationView):
    success_message_template = _('Seats successfully reserved.')
    form_class = ReservationForm
    template_name = 'paikkala_reservation_view.pug'

    def get_object(self, queryset=None):
        """
        The `programme_event_required` decorator adds `event` to kwargs.
        `programme_id`, referring to `programme.Programme`, comes from the URL.
        Using these, resolve and inject the `pk`, referring to `paikkala.Program`.
        """
        programme = self.get_programme()
        self.kwargs['pk'] = programme.paikkala_program_id
        return super().get_object(queryset)


    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        form.helper = horizontal_form_helper()
        form.helper.form_tag = False
        return form


paikkala_inspection_view = programme_event_required(InspectionView.as_view())
paikkala_relinquish_view = programme_event_required(RelinquishView.as_view())
paikkala_reservation_view = programme_event_required(ReservationView.as_view())
