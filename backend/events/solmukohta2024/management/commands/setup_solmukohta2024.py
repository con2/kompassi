import os
from datetime import datetime, timedelta

from dateutil.tz import tzlocal
from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils.timezone import now


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
        # self.setup_programme()
        self.setup_tickets()

    def setup_core(self):
        from core.models import Event, Organization, Venue

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

    def setup_programme(self):
        from core.utils import full_hours_between
        from labour.models import PersonnelClass
        from programme.models import (
            AlternativeProgrammeForm,
            Category,
            ProgrammeEventMeta,
            Role,
            SpecialStartTime,
            Tag,
            TimeBlock,
        )

        from ...models import ContentWarning, Documentation, Mentoring, PanelParticipation, Technology

        # make typechecker happy
        assert self.event.start_time
        assert self.event.end_time

        programme_admin_group, hosts_group = ProgrammeEventMeta.get_or_create_groups(self.event, ["admins", "hosts"])
        programme_event_meta, unused = ProgrammeEventMeta.objects.get_or_create(
            event=self.event,
            defaults=dict(
                public=False,
                admin_group=programme_admin_group,
                contact_email="Solmukohta programme <programme@solmukohta.eu>",
                schedule_layout="full_width",
            ),
        )

        if not programme_event_meta.override_schedule_link:
            programme_event_meta.override_schedule_link = "https://solmukohta.eu/programme/guide/#event:solmukohta"
            programme_event_meta.save(update_fields=["override_schedule_link"])

        if settings.DEBUG:
            programme_event_meta.accepting_cold_offers_from = now() - timedelta(days=60)
            programme_event_meta.accepting_cold_offers_until = now() + timedelta(days=60)
            programme_event_meta.save()

        for pc_slug, role_title, role_is_default in [
            ("programme", "Programme host", True),
        ]:
            personnel_class, _ = PersonnelClass.objects.get_or_create(
                event=self.event,
                slug=pc_slug,
                defaults=dict(
                    name=role_title,
                ),
            )
            Role.objects.get_or_create(
                personnel_class=personnel_class,
                title=role_title,
                defaults=dict(
                    is_default=role_is_default,
                    is_public=False,
                ),
            )

        for title, style in [
            ("Talk (lecture, lightning talks etc.)", "color1"),
            # ("Short talk", "color1"),
            ("Panel discussion", "color2"),
            ("Roundtable discussion", "color3"),
            ("Workshop", "color4"),
            ("Larp", "color5"),
            ("Show", "color7"),
            ("Social/party/ritual", "color6"),
            ("AWeek program", "color8"),
        ]:
            Category.objects.get_or_create(
                event=self.event,
                title=title,
                defaults=dict(
                    style=style,
                    public=title != "AWeek program",
                ),
            )

        for tag_title, tag_class in [
            ("A Week - Larp", "label-default"),
            ("A Week - Seminar", "label-default"),
            ("A Week - Visit", "label-default"),
            ("A Week - Workshop", "label-default"),
            ("A Week - Entertainment", "label-default"),
        ]:
            Tag.objects.get_or_create(
                event=self.event,
                title=tag_title,
                defaults=dict(
                    style=tag_class,
                ),
            )

        for start_time, end_time in [
            (
                self.event.start_time.replace(hour=10, minute=0, tzinfo=self.tz),
                self.event.end_time.replace(hour=20, minute=0, tzinfo=self.tz),
            ),
        ]:
            TimeBlock.objects.get_or_create(
                event=self.event,
                start_time=start_time,
                defaults=dict(end_time=end_time),
            )

        for time_block in TimeBlock.objects.filter(event=self.event):
            # Quarter or half hours
            # [:-1] – discard 18:00 to 19:00
            for hour_start_time in full_hours_between(time_block.start_time, time_block.end_time)[:-1]:
                # for minute in [15, 30, 45]:
                for minute in [30]:
                    SpecialStartTime.objects.get_or_create(
                        event=self.event,
                        start_time=hour_start_time.replace(minute=minute),
                    )

        sk_form, _ = AlternativeProgrammeForm.objects.get_or_create(
            event=self.event,
            slug="default",
            defaults=dict(
                title="Offer program for Solmukohta",
                short_description="The program is hosted at the Scandic Rosendahl hotel on October 11–14, 2024.",
                programme_form_code="events.solmukohta2024.forms:ProgrammeForm",
                num_extra_invites=0,
                order=10,
            ),
        )

        if sk_form.num_extra_invites > 0:
            sk_form.num_extra_invites = 0
            sk_form.save()

        a_form, _ = AlternativeProgrammeForm.objects.get_or_create(
            event=self.event,
            slug="aweek",
            defaults=dict(
                title="Offer program for A Week in Tampere",
                short_description="The program is hosted at Artteli or another venue in downtown Tampere on October 8–10, 2024.",
                programme_form_code="events.solmukohta2024.forms:AForm",
                num_extra_invites=0,
                order=20,
            ),
        )

        if a_form.num_extra_invites > 0:
            a_form.num_extra_invites = 0
            a_form.save()

        if a_form.programme_form_code == "events.solmukohta2024.forms:ProgrammeForm":
            a_form.programme_form_code = "events.solmukohta2024.forms:AForm"
            a_form.save()

        if not ContentWarning.objects.exists():
            for name in [
                "Loud noises (shouting, cheering, loud video, sound effects etc)",
                "Flashing lights",
                "Other content warnings (describe below)",
            ]:
                ContentWarning.objects.get_or_create(name=name)

        if not Documentation.objects.exists():
            for name in [
                "My programme item may be photographed",
                "My programme item may be streamed",
                "My programme may be video recorded",
                "My programme materials (slides, other documents) may be shared",
                "I don't want any documentation, thank you!",
            ]:
                Documentation.objects.get_or_create(name=name)

        if not PanelParticipation.objects.exists():
            for name in [
                "I am willing to participate in another host's panel discussion",
                "I am suggesting a panel item and would welcome panelist suggestions from the programme team",
            ]:
                PanelParticipation.objects.get_or_create(name=name)

        if not Mentoring.objects.exists():
            for name in [
                "I would like to have a mentor",
                "I am willing to mentor others",
            ]:
                Mentoring.objects.get_or_create(name=name)

        if not Technology.objects.exists():
            for name in [
                "Bringing my own laptop",
                "Need to borrow a laptop",
                "Projector / screen / TV",
                "Music / sound playback",
                "Special lighting",
                "Microphone(s)",
            ]:
                Technology.objects.get_or_create(name=name)

        self.event.programme_event_meta.create_groups()

    def setup_tickets(self):
        from tickets.models import LimitGroup, Product, TicketsEventMeta

        (tickets_admin_group,) = TicketsEventMeta.get_or_create_groups(self.event, ["admins"])

        defaults = dict(
            admin_group=tickets_admin_group,
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
        )

        if self.test:
            t = now()
            defaults.update(
                ticket_sales_starts=t - timedelta(days=60),  # type: ignore
                ticket_sales_ends=t + timedelta(days=60),  # type: ignore
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

        day_ticket_mail_description = "Next you need to fill in the sign-up form at https://forms.gle/grCULVpzz1rihnHZA. Please make note of your order number: you will need it while filling the form."

        for product_info in [
            dict(
                name="Suite ticket",
                description="The suite ticket includes <strong>two spots</strong> in the event. The 105&nbsp;m<sup>2</sup> suite has a separate bedroom and living room, two bathrooms, a private sauna and a balcony.",
                limit_groups=[
                    limit_group("Suite tickets", 1),
                ],
                price_cents=1600_00,
                electronic_ticket=False,
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
                electronic_ticket=False,
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
                electronic_ticket=False,
                available=True,
                ordering=ordering(),
            ),
            dict(
                name="Team ticket",
                description="This ticket type is intended for the <strong>Solmukohta team members</strong> and includes a spot in either a two-person or a three-person room.",
                limit_groups=[
                    limit_group("Team tickets", 25),
                ],
                price_cents=300_00,
                electronic_ticket=False,
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
                electronic_ticket=False,
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
                electronic_ticket=False,
                available=True,
                ordering=ordering(),
                code="communityhost-lksxrdjr",
            ),
            dict(
                name="Standard ticket",
                description="The standard ticket includes one spot in either a two-person or a three-person room.",
                limit_groups=[
                    limit_group("Standard tickets", 322),
                ],
                price_cents=400_00,
                electronic_ticket=False,
                available=True,
                ordering=ordering(),
            ),
            dict(
                name="Discount ticket",
                description="The discount ticket includes one spot in either a two-person or a three-person room. NOTE: Only purchase this if you have been specifically instucted to do so by the Solmukohta team. Only purchase one discount ticket for yourself.",
                limit_groups=[
                    limit_group("Discount tickets", 37),
                ],
                price_cents=250_00,
                electronic_ticket=False,
                available=True,
                ordering=ordering(),
                code="discount-rnndcwsb",
            ),
            dict(
                name="Single person room add-on",
                description="This add-on is for those who want to stay in a single person room. Note that in addition to this add-on, you will need to purchase a ticket for the event.",
                price_cents=200_00,
                electronic_ticket=False,
                available=True,
                ordering=ordering(),
                limit_groups=[
                    limit_group("Single person room add-ons", 10),
                ],
            ),
            dict(
                name="Day ticket – Friday",
                description="Friday ticket to Solmukohta. This ticket allows you to attend Solmukohta on Friday April 12. The ticket includes lunch and dinner, as well as any parties in the evening, but it does not include accommodation. For the ticket to be valid, you must fill in the sign-up form linked in the confirmation email within one week of purchase. You will have to show identification (ID card, passport or driver's license) at the info desk to get your badge.",
                mail_description=day_ticket_mail_description,
                price_cents=80_00,
                electronic_ticket=False,
                available=True,
                ordering=ordering(),
                limit_groups=[
                    limit_group("Friday tickets", 15),
                ],
            ),
            dict(
                name="Day ticket – Saturday",
                description="Saturday ticket to Solmukohta. This ticket allows you to attend Solmukohta on Saturday April 13. The ticket includes lunch and dinner, as well as any parties in the evening, but it does not include accommodation. For the ticket to be valid, you must fill in the sign-up form linked in the confirmation email within one week of purchase. You will have to show identification (ID card, passport or driver's license) at the info desk to get your badge.",
                mail_description=day_ticket_mail_description,
                price_cents=80_00,
                electronic_ticket=False,
                available=True,
                ordering=ordering(),
                limit_groups=[
                    limit_group("Saturday tickets", 15),
                ],
            ),
            dict(
                name="Day ticket – Friday and Saturday",
                description="Friday & Saturday ticket to Solmukohta at a small discount compared to purchasing Friday & Saturday separately. This ticket allows you to attend Solmukohta on Friday April 12 and Saturday April 13. The ticket includes lunch and dinner, as well as any parties in the evening, but it does not include accommodation. For the ticket to be valid, you must fill in the sign-up form linked in the confirmation email within one week of purchase. You will have to show identification (ID card, passport or driver's license) at the info desk to get your badge.",
                mail_description=day_ticket_mail_description,
                price_cents=140_00,
                electronic_ticket=False,
                available=True,
                ordering=ordering(),
                limit_groups=[
                    limit_group("Friday tickets", 15),
                    limit_group("Saturday tickets", 15),
                ],
            ),
            dict(
                name="Day ticket – Thursday",
                description="Thursday ticket to Solmukohta. This ticket allows you to attend Solmukohta on Thursday April 11. The ticket includes dinner, as well as any parties in the evening, but it does not include accommodation. For the ticket to be valid, you must fill in the sign-up form linked in the confirmation email within one week of purchase. You will have to show identification (ID card, passport or driver's license) at the info desk to get your badge.",
                mail_description=day_ticket_mail_description,
                price_cents=50_00,
                electronic_ticket=False,
                available=True,
                ordering=ordering(),
                limit_groups=[
                    limit_group("Thursday tickets", 5),
                ],
            ),
            dict(
                name="Day ticket – Sunday",
                description="Sunday ticket to Solmukohta. This ticket allows you to attend Solmukohta on Sunday April 14.",
                mail_description=day_ticket_mail_description,
                price_cents=40_00,
                electronic_ticket=False,
                available=True,
                ordering=ordering(),
                limit_groups=[
                    limit_group("Sunday tickets", 1),
                ],
            ),
            dict(
                name="Book – What Do We Do When We Play? (2020)",
                description=(
                    "ONLY FOR RETRIEVAL AT SOLMUKOHTA 2024. IF YOU CANNOT COME, HAVE A FRIEND PICK IT UP FROM THE INFO WITH THE RECEIPT. WE DO NOT MAIL BOOKS.\n\n"
                    "Over the course of thirty years, the Nordic larp community has learned a huge amount about the design and analysis of larps. Now, we open the next chapter and ask the question, “what do we do when we play?”\n\n"
                    "This book focuses on the experience, skills, and understanding of the participant. With 85 texts from 73 authors, we’re still just scratching the surface, but we hope that you'll find pieces in here that change the way you play and how you think about it."
                ),
                price_cents=25_00,
                electronic_ticket=False,
                available=True,
                ordering=ordering(),
                limit_groups=[
                    limit_group("2020 book", 12),
                ],
            ),
            dict(
                name="Book – Liminal Encounters (2024)",
                description=(
                    "ONLY FOR RETRIEVAL AT SOLMUKOHTA 2024. IF YOU CANNOT COME, HAVE A FRIEND PICK IT UP FROM THE INFO WITH THE RECEIPT. WE DO NOT MAIL BOOKS.\n\n"
                    "Do you want to know what is going on in larp and where the discourse is going? Read the Solmukohta 2024 book, Liminal Encounters: Evolving Discourse in Nordic and Nordic-inspired Larp. The book contains opinions and debate, concrete tips on how to make larps, and academic style analysis. At 400 pages, with 58 contributors, it both delivers fresh perspectives and further develops established theories."
                ),
                price_cents=25_00,
                electronic_ticket=False,
                available=True,
                ordering=ordering(),
                limit_groups=[
                    limit_group("2024 book", 24),
                ],
            ),
        ]:
            name = product_info.pop("name")
            limit_groups = product_info.pop("limit_groups")

            product, unused = Product.objects.get_or_create(event=self.event, name=name, defaults=product_info)

            if not product.limit_groups.exists():
                product.limit_groups.set(limit_groups)  # type: ignore
                product.save()


class Command(BaseCommand):
    args = ""
    help = "Setup solmukohta2024 specific stuff"

    def handle(self, *args, **opts):
        Setup().setup(test=settings.DEBUG)
