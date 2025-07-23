import logging
from functools import wraps

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from paikkala.excs import (
    BatchSizeOverflow,
    MaxTicketsPerUserReached,
    MaxTicketsReached,
    NoCapacity,
    NoRowCapacity,
    Unreservable,
    UserRequired,
)
from paikkala.views import (
    InspectionView as BaseInspectionView,
)
from paikkala.views import (
    RelinquishView as BaseRelinquishView,
)
from paikkala.views import (
    ReservationView as BaseReservationView,
)

from kompassi.core.utils import horizontal_form_helper
from kompassi.zombies.programme.models.special_reservation import SpecialReservation

from ..forms import ReservationForm
from ..helpers import programme_event_required
from ..models import Programme

logger = logging.getLogger(__name__)


class PaikkalAdapterMixin:
    """
    Translates between Kompassi and Paikkala.
    """

    def get_context_data(self, **kwargs):
        """
        Kompassi `base.pug` template needs `event`.
        """
        context = super().get_context_data(**kwargs)
        context["event"] = self.kwargs["event"]
        return context

    def get_programme(self):
        event = self.kwargs["event"]
        programme_id = self.kwargs["programme_id"]  # NOTE: programme.Programme, not paikkala.Program
        return get_object_or_404(
            Programme,
            id=int(programme_id),
            category__event=event,
            is_using_paikkala=True,
            paikkala_program__isnull=False,
        )

    def get_success_url(self):
        return reverse("programme:profile_reservations_view")


def handle_errors(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        # exc_info may only be called from inside exception handler
        # don't use logger.exception, it spams the admin
        try:
            return view_func(request, *args, **kwargs)

        except UserRequired:
            message = _("You need to log in before reserving tickets.")
            messages.error(request, message)
            logger.warning(message, exc_info=True)
            return redirect("core_frontpage_view")

        except BatchSizeOverflow:
            message = _("The size of your reservation exceeds the allowed maximum. Please try a smaller reservation.")
            messages.error(request, message)
            logger.warning(message, exc_info=True)
            return redirect(request.path)

        except MaxTicketsReached:
            message = _("This programme is currently full.")
            messages.error(request, message)
            logger.warning(message, exc_info=True)
            return redirect("programme:profile_reservations_view")

        except MaxTicketsPerUserReached:
            message = _("You cannot reserve any more tickets for this programme.")
            messages.error(request, message)
            logger.warning(message, exc_info=True)
            return redirect("programme:profile_reservations_view")

        except Unreservable:
            message = _("This programme does not allow reservations at this time.")
            messages.error(request, message)
            logger.warning(message, exc_info=True)
            return redirect("programme:profile_reservations_view")

        except PermissionDenied:
            message = _("Permission denied.")
            messages.error(request, message)
            logger.warning(message, exc_info=True)
            return redirect("core_frontpage_view")

        except (NoCapacity, NoRowCapacity):
            message = _(
                "There isn't sufficient space for your reservation in the selected zone. Please try another zone."
            )
            messages.error(request, message)
            logger.warning(message, exc_info=True)
            return redirect(request.path)

    return wrapper


class InspectionView(PaikkalAdapterMixin, BaseInspectionView):
    template_name = "programme_paikkala_inspection_view.pug"
    require_same_user = True
    require_same_zone = True


class RelinquishView(PaikkalAdapterMixin, BaseRelinquishView):
    success_message_template = _("Successfully relinquished the seat reservation.")


class ReservationView(PaikkalAdapterMixin, BaseReservationView):
    success_message_template = _("Seats successfully reserved.")
    form_class = ReservationForm
    template_name = "programme_paikkala_reservation_view.pug"

    def get_object(self, queryset=None):
        """
        The `programme_event_required` decorator adds `event` to kwargs.
        `programme_id`, referring to `programme.Programme`, comes from the URL.
        Using these, resolve and inject the `pk`, referring to `paikkala.Program`.
        """
        programme = self.get_programme()
        self.kwargs["pk"] = programme.paikkala_program_id
        return super().get_object(queryset)

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        form.helper = horizontal_form_helper()
        form.helper.form_tag = False
        return form


paikkala_inspection_view = login_required(programme_event_required(InspectionView.as_view()))
paikkala_relinquish_view = login_required(programme_event_required(handle_errors(RelinquishView.as_view())))
paikkala_reservation_view = login_required(programme_event_required(handle_errors(ReservationView.as_view())))


def paikkala_special_reservation_view(request, code):
    special_reservation = get_object_or_404(SpecialReservation, code=code)

    if special_reservation.program.invalid_after and now() >= special_reservation.program.invalid_after:
        messages.error(request, _("This ticket is no longer valid."))
        return redirect("programme:profile_reservations_view")

    vars = dict(
        event=special_reservation.program.kompassi_programme.event,
        ticket=special_reservation,  # HAX!
        tickets=special_reservation.get_fake_tickets(),
    )

    return render(request, "programme_paikkala_inspection_view.pug", vars)
