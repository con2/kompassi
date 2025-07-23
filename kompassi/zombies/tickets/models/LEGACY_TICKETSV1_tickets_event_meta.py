import logging

from django.contrib.postgres.fields import HStoreField
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from kompassi.core.models import ContactEmailMixin, EventMetaBase, contact_email_validator

logger = logging.getLogger(__name__)


class TicketsEventMeta(ContactEmailMixin, EventMetaBase):
    ticket_sales_starts = models.DateTimeField(
        verbose_name=_("Ticket sales starts"),
        null=True,
        blank=True,
    )

    ticket_sales_ends = models.DateTimeField(
        verbose_name=_("Ticket sales ends"),
        null=True,
        blank=True,
    )

    reference_number_template = models.CharField(
        max_length=31,
        default="{:04d}",
        verbose_name=_("Reference number template"),
        help_text=_("Uses Python .format() string formatting."),
    )

    contact_email = models.CharField(
        max_length=255,
        validators=[
            contact_email_validator,
        ],
        verbose_name=_("Contact e-mail address (with description)"),
        help_text=_("Format: Fooevent Ticket Sales &lt;tickets@fooevent.example.com&gt;"),
        blank=True,
    )

    ticket_free_text = models.TextField(
        blank=True,
        verbose_name=_("E-ticket text"),
        help_text=_("This text will be printed in the electronic ticket."),
    )

    front_page_text = models.TextField(
        blank=True,
        default="",
        verbose_name=_("Front page text"),
        help_text=_("This text will be shown on the front page of the web shop."),
    )

    print_logo_path = models.CharField(
        max_length=255,
        blank=True,
        default="",
        verbose_name=_("Logo path"),
        help_text=_("The file system path to a logo that will be printed on the electronic ticket."),
    )

    print_logo_width_mm = models.IntegerField(
        default=0,
        verbose_name=_("Logo width (mm)"),
        help_text=_(
            "The width of the logo to be printed on electronic tickets, in millimeters. Roughly 40 mm recommended."
        ),
    )

    print_logo_height_mm = models.IntegerField(
        default=0,
        verbose_name=_("Logo height (mm)"),
        help_text=_(
            "The height of the logo to be printed on electronic tickets, in millimeters. Roughly 20 mm recommended."
        ),
    )

    pos_access_group = models.ForeignKey(
        "auth.Group",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("POS access group"),
        help_text=_(
            "Members of this group are granted access to the ticket exchange view without being ticket admins."
        ),
        related_name="as_pos_access_group_for",
    )

    terms_and_conditions_url = HStoreField(blank=True, default=dict)

    max_count_per_product = models.SmallIntegerField(blank=True, default=99)

    def __str__(self):
        return self.event.name

    @property
    def print_logo_size_cm(self):
        return (self.print_logo_width_mm / 10.0, self.print_logo_height_mm / 10.0)

    @property
    def is_ticket_sales_open(self):
        t = timezone.now()

        # Starting date must be set for the ticket sales to be considered open
        if not self.ticket_sales_starts:
            return False

        # Starting date must be in the past for the ticket sales to be considered open
        if self.ticket_sales_starts > t:
            return False

        # If there is an ending date, it must not have been passed yet
        if self.ticket_sales_ends:
            return t <= self.ticket_sales_ends

        return True

    @classmethod
    def get_or_create_dummy(cls):
        from django.contrib.auth.models import Group

        from kompassi.core.models import Event

        group, unused = Group.objects.get_or_create(name="Dummy ticket admin group")
        event, unused = Event.get_or_create_dummy()
        return cls.objects.get_or_create(event=event, defaults=dict(admin_group=group))

    def is_user_allowed_pos_access(self, user):
        if self.is_user_admin(user):
            return True

        return self.pos_access_group and self.is_user_in_group(user, self.pos_access_group)

    class Meta:
        verbose_name = _("ticket sales settings for event")
        verbose_name_plural = _("ticket sales settings for events")
