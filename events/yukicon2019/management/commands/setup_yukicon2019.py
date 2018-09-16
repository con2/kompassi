import os
from datetime import datetime, timedelta

from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils.timezone import now

from dateutil.tz import tzlocal

from core.utils import slugify


def mkpath(*parts):
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', *parts))


class Setup(object):
    def __init__(self):
        self._ordering = 0

    def get_ordering_number(self):
        self._ordering += 10
        return self._ordering

    def setup(self, test=False):
        self.test = test
        self.tz = tzlocal()
        self.setup_core()
        # self.setup_tickets()
        # self.setup_payments()
        self.setup_labour()
        # self.setup_programme()
        self.setup_badges()
        self.setup_intra()

    def setup_core(self):
        from core.models import Venue, Event

        self.venue, unused = Venue.objects.get_or_create(name='Messukeskus Siipi', defaults=dict(
            name_inessive='Messukeskus Siivessä',
        ))
        self.event, unused = Event.objects.get_or_create(slug='yukicon2019', defaults=dict(
            name='Yukicon 6.0 (2019)',
            name_genitive='Yukicon 6.0 -tapahtuman',
            name_illative='Yukicon 6.0 -tapahtumaan',
            name_inessive='Yukicon 6.0 -tapahtumassa',
            homepage_url='http://www.yukicon.fi',
            organization_name='Yukitea ry',
            organization_url='http://www.yukicon.fi',
            start_time=datetime(2019, 3, 9, 10, 0, tzinfo=self.tz),
            end_time=datetime(2019, 3, 10, 18, 0, tzinfo=self.tz),
            venue=self.venue,
            panel_css_class='panel-info',
        ))

    def setup_tickets(self):
        from tickets.models import TicketsEventMeta, LimitGroup, Product

        tickets_admin_group, = TicketsEventMeta.get_or_create_groups(self.event, ['admins'])

        defaults = dict(
            admin_group=tickets_admin_group,
            due_days=14,
            shipping_and_handling_cents=0,
            reference_number_template="2019{:05d}",
            contact_email='Yukicon <yukicon@yukicon.fi>',
            ticket_free_text=(
                "Tämä on sähköinen lippusi. Sähköinen lippu vaihdetaan rannekkeeseen\n"
                "lipunvaihtopisteessä saapuessasi tapahtumaan. Voit tulostaa tämän lipun tai näyttää sen\n"
                "älypuhelimen tai tablettitietokoneen näytöltä. Mikäli kumpikaan näistä ei ole mahdollista, ota ylös\n"
                "kunkin viivakoodin alla oleva neljästä tai viidestä sanasta koostuva sanakoodi ja ilmoita se\n"
                "lipunvaihtopisteessä.\n\n"
                "Tervetuloa tapahtumaan!"
            ),
            front_page_text=(
                "<h2>Tervetuloa ostamaan pääsylippuja Yukicon 6.0-tapahtumaan!</h2>"
                "<p>Liput maksetaan suomalaisilla verkkopankkitunnuksilla heti tilauksen yhteydessä.</p>"
                "<p>Lue lisää tapahtumasta "
                "<a href='http://www.yukicon.fi' target='_blank'>Yukiconin kotisivuilta</a>.</p>"
            ),
            print_logo_path=mkpath('static', 'images', 'Yukicon_logo_taustaton.jpg'),
            print_logo_width_mm=50,
            print_logo_height_mm=16
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

        for product_info in [
            dict(
                name='Yukicon 6.0 – Early Access',
                description=(
                    'Early Access -lipulla pääset Yukiconiin TODO PÄIVÄMÄÄRÄT. Lippu oikeuttaa Early Access '
                    '-etuuksien lunastuksen. Maksettuasi sinulle lähetetään PDF-lippu antamaasi sähköpostiin, '
                    'jota vastaan saat rannekkeen tapahtuman ovelta.'
                ),
                limit_groups=[
                    limit_group('Early Access', 200),
                ],
                price_cents=2900,
                requires_shipping=False,
                electronic_ticket=True,
                available=True,
                ordering=self.get_ordering_number(),
            ),
        ]:
            name = product_info.pop('name')
            limit_groups = product_info.pop('limit_groups')

            product, unused = Product.objects.get_or_create(
                event=self.event,
                name=name,
                defaults=product_info
            )

            if not product.limit_groups.exists():
                product.limit_groups = limit_groups
                product.save()

    def setup_payments(self):
        from payments.models import PaymentsEventMeta
        PaymentsEventMeta.get_or_create_dummy(event=self.event)

    def setup_programme(self):
        from labour.models import PersonnelClass
        from programme.models import (
            Category,
            ProgrammeEventMeta,
            Role,
            Room,
            SpecialStartTime,
            Tag,
            TimeBlock,
            View,
        )
        from core.utils import full_hours_between

        for room_name in [
            '207',
            '208',
            '209',
            '205',
            'Iso sali',
        ]:
            Room.objects.get_or_create(event=self.event, name=room_name)

        admin_group, hosts_group = ProgrammeEventMeta.get_or_create_groups(self.event, ['admins', 'hosts'])
        programme_event_meta, unused = ProgrammeEventMeta.objects.get_or_create(event=self.event, defaults=dict(
            admin_group=admin_group,
        ))

        if not programme_event_meta.contact_email:
            programme_event_meta.contact_email = 'Yukiconin ohjelmavastaava <ohjelma@yukicon.fi>'
            programme_event_meta.save()

        if settings.DEBUG:
            programme_event_meta.accepting_cold_offers_from = now() - timedelta(days=60)
            programme_event_meta.accepting_cold_offers_until = now() + timedelta(days=60)
            programme_event_meta.save()

        for pc_slug, role_title, role_is_default in [
            ('ohjelma', 'Ohjelmanjärjestäjä', True),
        ]:
            personnel_class = PersonnelClass.objects.get(event=self.event, slug=pc_slug)
            role, unused = Role.objects.get_or_create(
                personnel_class=personnel_class,
                title=role_title,
                defaults=dict(
                    is_default=role_is_default,
                )
            )

        view, unused = View.objects.get_or_create(
            event=self.event,
            name='Ohjelmakartta',
        )

        if not view.rooms.exists():
            view.rooms = Room.objects.filter(event=self.event)
            view.save()

        for category_name, category_style in [
            ('Pelit', 'rope'),
            ('Anime/manga', 'anime'),
            ('Cosplay', 'cosplay'),
            ('Muu', 'muu'),
        ]:
            Category.objects.get_or_create(
                event=self.event,
                title=category_name,
                defaults=dict(
                    style=category_style,
                )
            )

        for tag_name, tag_style in [
            ('Luento', 'label-default'),
            ('Paneeli', 'label-success'),
            ('Keskustelupiiri', 'label-info'),
            ('Työpaja', 'label-warning'),
            ("Let's Play", 'label-danger'),
            ('Visa/leikki', 'label-primary'),
        ]:
            Tag.objects.get_or_create(
                event=self.event,
                title=tag_name,
                defaults=dict(
                    style=tag_style,
                ),
            )

        if not TimeBlock.objects.filter(event=self.event).exists():
            for start_time, end_time in [
                (
                    self.event.start_time,
                    self.event.start_time.replace(hour=22, tzinfo=self.tz),
                ),
                (
                    self.event.end_time.replace(hour=9, tzinfo=self.tz),
                    self.event.end_time,
                ),
            ]:
                TimeBlock.objects.get_or_create(
                    event=self.event,
                    start_time=start_time,
                    defaults=dict(
                        end_time=end_time
                    )
                )

        for time_block in TimeBlock.objects.filter(event=self.event):
            # Half hours
            # [:-1] – discard 18:30
            for hour_start_time in full_hours_between(time_block.start_time, time_block.end_time)[:-1]:
                SpecialStartTime.objects.get_or_create(
                    event=self.event,
                    start_time=hour_start_time.replace(minute=30)
                )

    def setup_labour(self):
        from core.models import Event, Person
        from labour.models import (
            AlternativeSignupForm,
            InfoLink,
            JobCategory,
            LabourEventMeta,
            PersonnelClass,
            Qualification,
        )
        from ...models import SignupExtra, SpecialDiet, EventDay
        from django.contrib.contenttypes.models import ContentType

        labour_admin_group, = LabourEventMeta.get_or_create_groups(self.event, ['admins'])

        if self.test:
            person, unused = Person.get_or_create_dummy()
            labour_admin_group.user_set.add(person.user)

        content_type = ContentType.objects.get_for_model(SignupExtra)

        labour_event_meta_defaults = dict(
            signup_extra_content_type=content_type,
            # work_begins=self.event.start_time - timedelta(days=1),
            # work_ends=self.event.end_time + timedelta(hours=4),
            work_begins=datetime(2019, 2, 1, 0, 0, 0, tzinfo=self.tz),
            work_ends=datetime(2019, 3, 31, 0, 0, 0, tzinfo=self.tz),
            admin_group=labour_admin_group,
            contact_email='Yukiconin työvoimatiimi <yukicon@yukicon.fi>',
        )

        if self.test:
            t = now()
            labour_event_meta_defaults.update(
                registration_opens=t - timedelta(days=60),
                registration_closes=t + timedelta(days=60),
            )
        else:
            pass

        labour_event_meta, unused = LabourEventMeta.objects.get_or_create(
            event=self.event,
            defaults=labour_event_meta_defaults,
        )

        for pc_name, pc_slug, pc_app_label in [
            ('Conitea', 'conitea', 'labour'),
            ('Työvoima', 'tyovoima', 'labour'),
            ('Ohjelmanjärjestäjä', 'ohjelma', 'programme'),
            ('Media', 'media', 'badges'),
            ('Myyjä', 'myyja', 'badges'),
            ('Vieras', 'vieras', 'badges'),
        ]:
            personnel_class, created = PersonnelClass.objects.get_or_create(
                event=self.event,
                slug=pc_slug,
                defaults=dict(
                    name=pc_name,
                    app_label=pc_app_label,
                    priority=self.get_ordering_number(),
                ),
            )

        tyovoima = PersonnelClass.objects.get(event=self.event, slug='tyovoima')
        conitea = PersonnelClass.objects.get(event=self.event, slug='conitea')

        # for name, description, pcs in [
        #     (
        #         'Conitea',
        #         'Tapahtuman järjestelytoimikunnan jäsen eli conitea',
        #         [conitea]
        #     ),
        #     (
        #         'Järjestyksenvalvoja',
        #         'Kävijöiden turvallisuuden valvominen conipaikalla ja yömajoituksessa. Edellyttää voimassa olevaa '
        #         'JV-korttia ja asiakaspalveluasennetta. HUOM! Et voi valita tätä tehtävää hakemukseesi, ellet ole '
        #         'täyttänyt tietoihisi JV-kortin numeroa (oikealta ylhäältä oma nimesi &gt; Pätevyydet).',
        #         [tyovoima]
        #     ),
        # ]:
        #     job_category, created = JobCategory.objects.get_or_create(
        #         event=self.event,
        #         slug=slugify(name),
        #         defaults=dict(
        #             name=name,
        #             description=description,
        #         )
        #     )

        #     if created:
        #         job_category.personnel_classes = pcs
        #         job_category.save()

        if not JobCategory.objects.filter(event=self.event).exists():
            JobCategory.copy_from_event(
                source_event=Event.objects.get(slug='yukicon2018'),
                target_event=self.event,
            )

        for name in ['Conitea']:
            JobCategory.objects.filter(event=self.event, name=name).update(public=False)

        for jc_name, qualification_name in [
            ('Järjestyksenvalvoja', 'JV-kortti'),
        ]:
            jc = JobCategory.objects.get(event=self.event, name=jc_name)
            qual = Qualification.objects.get(name=qualification_name)

            jc.required_qualifications = [qual]
            jc.save()

        labour_event_meta.create_groups()

        for diet_name in [
            'Gluteeniton',
            'Laktoositon',
            'Maidoton',
            'Vegaaninen',
            'Lakto-ovo-vegetaristinen',
        ]:
            SpecialDiet.objects.get_or_create(name=diet_name)

        for event_day in [
            'Perjantai (rakennuspäivä)',
            'Lauantai',
            'Sunnuntai',
        ]:
            EventDay.objects.get_or_create(name=event_day)

        AlternativeSignupForm.objects.get_or_create(
            event=self.event,
            slug='conitea',
            defaults=dict(
                title='Conitean ilmoittautumislomake',
                signup_form_class_path='events.yukicon2019.forms:OrganizerSignupForm',
                signup_extra_form_class_path='events.yukicon2019.forms:OrganizerSignupExtraForm',
                active_from=datetime(2018, 4, 26, 0, 0, 0, tzinfo=self.tz),
                active_until=self.event.start_time,
            ),
        )

        for wiki_space, link_title, link_group in [
            ('YUKICON2019', 'Coniteawiki', 'conitea'),
            # ('YUKIWORK', 'Työvoimawiki', 'accepted'),
            # ('YUKINFO', 'Infowiki', 'info'),
        ]:
            InfoLink.objects.get_or_create(
                event=self.event,
                title=link_title,
                defaults=dict(
                    url='https://confluence.tracon.fi/display/{wiki_space}'.format(wiki_space=wiki_space),
                    group=labour_event_meta.get_group(link_group),
                )
            )

    def setup_badges(self):
        from badges.models import BadgesEventMeta

        badge_admin_group, = BadgesEventMeta.get_or_create_groups(self.event, ['admins'])
        meta, unused = BadgesEventMeta.objects.get_or_create(
            event=self.event,
            defaults=dict(
                admin_group=badge_admin_group,
                badge_layout='nick',
            )
        )

    def setup_intra(self):
        from intra.models import IntraEventMeta, Team

        admin_group, = IntraEventMeta.get_or_create_groups(self.event, ['admins'])
        organizer_group = self.event.labour_event_meta.get_group('conitea')
        meta, unused = IntraEventMeta.objects.get_or_create(
            event=self.event,
            defaults=dict(
                admin_group=admin_group,
                organizer_group=organizer_group,
            )
        )

        for team_slug, team_name in [
            ('pirut', 'Pirut'),
            ('ohjelma', 'Ohjelma'),
            ('tuotanto', 'Tuotanto'),
            ('talous', 'Talous'),
            ('tiedotus', 'Tiedotus'),
        ]:
            team_group, = IntraEventMeta.get_or_create_groups(self.event, [team_slug])
            email = '{}@yukicon.fi'.format(team_slug)

            team, created = Team.objects.get_or_create(
                event=self.event,
                slug=team_slug,
                defaults=dict(
                    name=team_name,
                    order=self.get_ordering_number(),
                    group=team_group,
                    email=email
                )
            )



class Command(BaseCommand):
    args = ''
    help = 'Setup yukicon2019 specific stuff'

    def handle(self, *args, **opts):
        Setup().setup(test=settings.DEBUG)
