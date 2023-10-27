import os
from datetime import datetime, timedelta

from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils.timezone import now

from dateutil.tz import tzlocal

from core.utils import slugify


def mkpath(*parts):
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", *parts))


class Setup:
    def __init__(self):
        self._ordering = 0

    def get_ordering_number(self):
        self._ordering += 10
        return self._ordering

    def setup(self, test=False):
        self.test = test
        self.tz = tzlocal()
        self.setup_core()
        self.setup_tickets()

    def setup_core(self):
        from core.models import Venue, Event, Organization

        self.venue, unused = Venue.objects.get_or_create(
            name="Scandic Rosendahl (Tampere)",
            defaults=dict(
                name_inessive="Scandic Rosendahlissa Tampereella",
            ),
        )
        self.organization, unused = Organization.objects.get_or_create(
            slug="ropecon-ry",
            defaults=dict(
                name="Ropecon ry",
                homepage_url="https://ry.ropecon.fi",
            ),
        )
        self.event, unused = Event.objects.get_or_create(
            slug="solmukohta2024",
            defaults=dict(
                name="Solmukohta 2024",
                name_genitive="Solmukohdan",
                name_illative="Solmukohtaan",
                name_inessive="Solmukohdassa",
                homepage_url="https://solmukohta.eu",
                organization=self.organization,
                start_time=datetime(2024, 10, 11, 15, 0, tzinfo=self.tz),
                end_time=datetime(2024, 10, 14, 15, 0, tzinfo=self.tz),
                venue=self.venue,
            ),
        )

    def setup_tickets(self):
        from tickets.models import TicketsEventMeta, LimitGroup, Product

        (tickets_admin_group,) = TicketsEventMeta.get_or_create_groups(self.event, ["admins"])

        defaults = dict(
            admin_group=tickets_admin_group,
            due_days=14,
            reference_number_template="2023{:05d}",
            contact_email="Solmukohta 2024 <tickets@solmukohta.eu>",
            ticket_free_text="This is your electronic ticket for Solmukohta 2024.\n"
            "You can show it on your mobile device or print it.\n"
            "Welcome to Solmukohta 2024!",
            front_page_text="""
<h1>Welcome to Solmukohta 2024 ticket shop!</h1>
<p>Sign up to Solmukohta 2024 happens by purchasing a ticket to the event. When you purchase your ticket in the Kompassi web store, you will be prompted to fill in a sign up form. For the suite and business tickets, you will need to enter the information for both attendees, as these ticket types include two spots in the event. Any placeholder tickets with incomplete information will be cancelled. If you purchase a ticket for someone else, make sure to forward the ticket to the ticket holder as they will need the order number to fill in the sign up form.</p>
<p>After completing the purchase a receipt and the ticket will be emailed to the address provided. Double check that you type in the correct email address!</p>
<p>For faster check in at the Solmukohta 2024 event, we ask all participants to have their identification ready at check in.</p>
""",
            tickets_view_version="v1.5",
        )

        if self.test:
            t = now()
            defaults.update(
                ticket_sales_starts=t - timedelta(days=60),
                ticket_sales_ends=t + timedelta(days=60),
            )

        meta, unused = TicketsEventMeta.objects.get_or_create(event=self.event, defaults=defaults)

        def limit_group(description, limit):
            limit_group, unused = LimitGroup.objects.get_or_create(
                event=self.event,
                description=description,
                defaults=dict(limit=limit),
            )

            return limit_group

        def ordering():
            ordering.counter += 10
            return ordering.counter

        ordering.counter = 0

        for product_info in [
            dict(
                name="Suite ticket",
                description="The suite ticket includes <strong>two spots</strong> in the event. The 105&nbsp;m<sup>2</sup> suite has a separate bedroom and living room, two bathrooms, a private sauna and a balcony.",
                limit_groups=[
                    limit_group("Suite tickets", 1),
                ],
                price_cents=1600_00,
                electronic_ticket=True,
                available=True,
                ordering=ordering(),
            ),
            dict(
                name="Business ticket",
                description="The business ticket includes <strong>two spots</strong> in the event. The 56 to 72&nbsp;m<sup>2</sup> rooms have a separate bedroom and living room.",
                limit_groups=[
                    limit_group("Business tickets", 5),
                ],
                price_cents=1400_00,
                electronic_ticket=True,
                available=True,
                ordering=ordering(),
            ),
            dict(
                name="Sponsor ticket",
                description="The sponsor ticket includes one spot in either a two-person or a three-person room.",
                limit_groups=[
                    limit_group("Sponsor tickets", 200),
                ],
                price_cents=550_00,
                electronic_ticket=True,
                available=True,
                ordering=ordering(),
            ),
            # dict(
            #     name="Standard ticket",
            #     description="The standard ticket includes one spot in either a two-person or a three-person room.",
            #     limit_groups=[
            #         limit_group("Standard tickets", 412 - 2 * y),
            #     ],
            #     price_cents=400_00,
            #     electronic_ticket=True,
            #     available=True,
            #     ordering=ordering(),
            # ),
            # dict(
            #     name="Discount ticket",
            #     description="The discount ticket includes one spot in either a two-person or a three-person room.",
            #     limit_groups=[
            #         limit_group("Discount tickets", y),
            #     ],
            #     price_cents=250_00,
            #     electronic_ticket=True,
            #     available=True,
            #     ordering=ordering(),
            # ),
            dict(
                name="Team ticket",
                description="This ticket type is intended for the <strong>Solmukohta team members</strong> and includes a spot in either a two-person or a three-person room.",
                limit_groups=[
                    limit_group("Team tickets", 25),
                ],
                price_cents=300_00,
                electronic_ticket=True,
                available=True,
                ordering=ordering(),
                code="team-nlxsddxt",
            ),
            dict(
                name="Volunteer ticket",
                description="This ticket type is intended for <strong>volunteers of Solmukohta</strong> and includes a spot in either a two-person or a three-person room.",
                limit_groups=[
                    limit_group("Volunteer tickets", 15),
                ],
                price_cents=350_00,
                electronic_ticket=True,
                available=True,
                ordering=ordering(),
                code="volunteer-nxwsphnd",
            ),
            dict(
                name="Community host ticket",
                description="This ticket type is intended for <strong>community hosts of Solmukohta</strong> and includes a spot in either a two-person or a three-person room.",
                limit_groups=[
                    limit_group("Community host tickets", 12),
                ],
                price_cents=400_00,
                electronic_ticket=True,
                available=True,
                ordering=ordering(),
                code="communityhost-lksxrdjr",
            ),
        ]:
            name = product_info.pop("name")
            limit_groups = product_info.pop("limit_groups")

            product, unused = Product.objects.get_or_create(
                event=self.event, name=name, defaults=product_info
            )

            if not product.limit_groups.exists():
                product.limit_groups.set(limit_groups)
                product.save()


class Command(BaseCommand):
    args = ""
    help = "Setup solmukohta2024 specific stuff"

    def handle(self, *args, **opts):
        Setup().setup(test=settings.DEBUG)
