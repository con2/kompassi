from dataclasses import dataclass

from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from kompassi.access.utils import generate_machine_password


@dataclass(frozen=True)
class FakeRow:
    name: str


@dataclass(frozen=True)
class FakeTicket:
    row: FakeRow
    number: str


def get_code():
    return generate_machine_password(num_chars=8)


class SpecialReservation(models.Model):
    """
    A "special reservation" provides a link that can be given to a privileged
    group of people. When opened, that link will then display an inspection
    view that looks like the inspection view of an ordinary seat reservation.
    Row and seat number will be overridden.

    Kindly please use the description field to tell whom & why this is for.
    """

    code = models.CharField(max_length=63, unique=True, default=get_code)
    program = models.ForeignKey("paikkala.Program", on_delete=models.CASCADE)
    zone = models.ForeignKey("paikkala.Zone", on_delete=models.CASCADE)
    row_name = models.CharField(max_length=255)
    seat_number = models.CharField(max_length=255, default="Numeroimaton")
    description = models.TextField()

    def get_fake_tickets(self):
        return [FakeTicket(row=FakeRow(self.row_name), number=self.seat_number)]

    def get_absolute_url(self):
        return reverse("program_v2:paikkala_special_reservation_view", kwargs=dict(code=self.code))

    @property
    def event(self):
        return self.program.kompassi_programme.event

    def admin_get_event(self):
        return self.event

    admin_get_event.short_description = _("Event")
    admin_get_event.admin_order_field = "program__kompassi_programme__category__event"
