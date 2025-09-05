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
from paikkala.models import Ticket
from paikkala.views import (
    InspectionView as BaseInspectionView,
)
from paikkala.views import (
    RelinquishView as BaseRelinquishView,
)
from paikkala.views import (
    ReservationView as BaseReservationView,
)

from kompassi.core.models.event import Event
from kompassi.core.utils import horizontal_form_helper
from kompassi.program_v2.models.schedule_item import ScheduleItem

from ..integrations.paikkala_integration import FakeTicket, ReservationForm

logger = logging.getLogger(__name__)


class PaikkalAdapterMixin:
    """
    Translates between Kompassi and Paikkala.
    """

    def get_context_data(self, **kwargs):
        """
        Kompassi `base.pug` template needs `event`.
        """
        context = super().get_context_data(**kwargs)  # type: ignore
        context["event"] = get_object_or_404(Event, slug=self.kwargs["event_slug"])  # type: ignore
        return context

    def get_schedule_item(self):
        event = get_object_or_404(Event, slug=self.kwargs["event_slug"])  # type: ignore
        schedule_item_slug = self.kwargs["schedule_item_slug"]  # type: ignore
        return get_object_or_404(
            ScheduleItem,
            program__event=event,
            slug=schedule_item_slug,
            cached_combined_dimensions__contains=dict(paikkala=[]),
        )

    def get_success_url(self):
        return reverse("program_v2:paikkala_profile_reservations_view")


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
            message = _("This program is currently full.")
            messages.error(request, message)
            logger.warning(message, exc_info=True)
            return redirect("program_v2:paikkala_profile_reservations_view")

        except MaxTicketsPerUserReached:
            message = _("You cannot reserve any more tickets for this schedule_item.")
            messages.error(request, message)
            logger.warning(message, exc_info=True)
            return redirect("program_v2:paikkala_profile_reservations_view")

        except Unreservable:
            message = _("This program does not allow reservations at this time.")
            messages.error(request, message)
            logger.warning(message, exc_info=True)
            return redirect("program_v2:paikkala_profile_reservations_view")

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
    template_name = "program_v2_paikkala_inspection_view.pug"
    require_same_user = True
    require_same_zone = True


class RelinquishView(PaikkalAdapterMixin, BaseRelinquishView):
    success_message_template = _("Successfully relinquished the seat reservation.")


class ReservationView(PaikkalAdapterMixin, BaseReservationView):
    success_message_template = _("Seats successfully reserved.")
    form_class = ReservationForm
    template_name = "program_v2_paikkala_reservation_view.pug"

    def get_object(self, queryset=None):
        schedule_item = self.get_schedule_item()
        self.kwargs["pk"] = schedule_item.paikkala_program_id
        return super().get_object(queryset)

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        form.helper = horizontal_form_helper()
        form.helper.form_tag = False
        return form


paikkala_inspection_view = login_required(InspectionView.as_view())
paikkala_relinquish_view = login_required(handle_errors(RelinquishView.as_view()))
paikkala_reservation_view = login_required(handle_errors(ReservationView.as_view()))


def paikkala_special_reservation_view(request, code):
    schedule_item = get_object_or_404(
        ScheduleItem,
        paikkala_special_reservation_code=code,
        cached_combined_dimensions__contains=dict(paikkala=[]),
    )

    paikkala_program = schedule_item.paikkala_program
    if not paikkala_program:
        logger.error(
            f"ScheduleItem {schedule_item.id} has no PaikkalaProgram despite having a special reservation code ({code})"
        )
        messages.error(request, _("This ticket is no longer valid."))
        return redirect("program_v2:paikkala_profile_reservations_view")

    if schedule_item.cached_end_time < now():
        messages.error(request, _("This ticket is no longer valid."))
        return redirect("program_v2:paikkala_profile_reservations_view")

    ticket = FakeTicket.for_paikkala_program(paikkala_program)

    vars = dict(
        event=schedule_item.event,
        ticket=ticket,  # HAX!
        tickets=[ticket],
    )

    return render(request, "program_v2_paikkala_inspection_view.pug", vars)


@login_required
def paikkala_profile_reservations_view(request):
    t = now()
    valid_tickets = Ticket.objects.valid().filter(user=request.user)  # type: ignore
    past_tickets = Ticket.objects.filter(user=request.user).exclude(id__in=valid_tickets)

    reservable_schedule_items = ScheduleItem.objects.filter(
        cached_combined_dimensions__contains=dict(paikkala=[]),
        paikkala_program__reservation_start__lte=t,
        paikkala_program__reservation_end__gt=t,
        is_public=True,
    )

    vars = dict(
        valid_tickets=valid_tickets,
        past_tickets=past_tickets,
        reservable_schedule_items=reservable_schedule_items,
    )

    return render(request, "program_v2_paikkala_profile_reservations_view.pug", vars)
