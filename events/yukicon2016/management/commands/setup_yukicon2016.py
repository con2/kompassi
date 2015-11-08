# encoding: utf-8

import os
from datetime import datetime, timedelta

from django.core.management.base import BaseCommand, make_option
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
        self.setup_tickets()
        self.setup_payments()
        self.setup_labour()
        self.setup_badges()

    def setup_core(self):
        from core.models import Venue, Event

        self.venue, unused = Venue.objects.get_or_create(name='Messukeskuksen Kokoustamo', defaults=dict(
            name_inessive='Messukeskuksen Kokoustamossa',
        ))
        self.event, unused = Event.objects.get_or_create(slug='yukicon2016', defaults=dict(
            name='Yukicon 3.0',
            name_genitive='Yukicon 3.0 -tapahtuman',
            name_illative='Yukicon 3.0 -tapahtumaan',
            name_inessive='Yukicon 3.0 -tapahtumassa',
            homepage_url='http://www.yukicon.fi',
            organization_name='Yukitea ry',
            organization_url='http://www.yukicon.fi',
            start_time=datetime(2016, 2, 27, 10, 0, tzinfo=self.tz),
            end_time=datetime(2016, 2, 28, 18, 0, tzinfo=self.tz),
            venue=self.venue,
        ))

    def setup_tickets(self):
        from tickets.models import TicketsEventMeta, LimitGroup, Product

        tickets_admin_group, = TicketsEventMeta.get_or_create_groups(self.event, ['admins'])

        defaults = dict(
            admin_group=tickets_admin_group,
            due_days=14,
            shipping_and_handling_cents=0,
            reference_number_template="2016{:05d}",
            contact_email='Yukicon <yukicon@yukicon.fi>',
            plain_contact_email='yukicon@yukicon.fi',
            ticket_free_text=u"Tämä on sähköinen lippusi Yukicon 3.0 -tapahtumaan. Sähköinen lippu vaihdetaan rannekkeeseen\n"
                u"lipunvaihtopisteessä saapuessasi tapahtumaan. Voit tulostaa tämän lipun tai näyttää sen\n"
                u"älypuhelimen tai tablettitietokoneen näytöltä. Mikäli kumpikaan näistä ei ole mahdollista, ota ylös\n"
                u"kunkin viivakoodin alla oleva neljästä tai viidestä sanasta koostuva sanakoodi ja ilmoita se\n"
                u"lipunvaihtopisteessä.\n\n"
                u"Tervetuloa Yukiconiin!",
            front_page_text=u"<h2>Tervetuloa ostamaan pääsylippuja Yukicon 3.0 -tapahtumaan!</h2>"
                u"<p>Liput maksetaan suomalaisilla verkkopankkitunnuksilla heti tilauksen yhteydessä.</p>"
                u"<p>Lue lisää tapahtumasta <a href='http://www.yukicon.fi' target='_blank'>Yukiconin kotisivuilta</a>.</p>",
            print_logo_path=mkpath('static', 'images', 'yukicon_436_test.jpg'),
            print_logo_width_mm=50,
            print_logo_height_mm=10
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
                name=u'Yukicon 3.0 -pääsylippu',
                description=u'Lippu kattaa koko viikonlopun. Maksettuasi sinulle lähetetään PDF-lippu antamaasi sähköpostiin, jota vastaan saat rannekkeen tapahtuman ovelta.',
                limit_groups=[
                    limit_group('Pääsyliput', 2400),
                ],
                price_cents=2500,
                requires_shipping=False,
                electronic_ticket=True,
                available=True,
                ordering=ordering(),
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

    def setup_labour(self):
        from core.models import Person
        from labour.models import (
            AlternativeSignupForm,
            InfoLink,
            Job,
            JobCategory,
            LabourEventMeta,
            Perk,
            PersonnelClass,
            Qualification,
            WorkPeriod,
        )
        from ...models import SignupExtra, SpecialDiet
        from django.contrib.contenttypes.models import ContentType

        labour_admin_group, = LabourEventMeta.get_or_create_groups(self.event, ['admins'])

        if self.test:
            from core.models import Person
            person, unused = Person.get_or_create_dummy()
            labour_admin_group.user_set.add(person.user)

        content_type = ContentType.objects.get_for_model(SignupExtra)

        labour_event_meta_defaults = dict(
            signup_extra_content_type=content_type,
            work_begins=self.event.start_time - timedelta(days=1),
            work_ends=self.event.end_time + timedelta(hours=4),
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
            (u'Conitea', 'conitea', 'labour'),
            (u'Työvoima', 'tyovoima', 'labour'),
            (u'Ohjelmanjärjestäjä', 'ohjelma', 'programme'),
            (u'Media', 'media', 'badges'),
            (u'Myyjä', 'myyja', 'badges'),
            (u'Vieras', 'vieras', 'badges'),
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

        for jc_data in [
            (
                u'Conitea',
                u'Tapahtuman järjestelytoimikunnan eli conitean jäsen',
                [conitea]
            ),
            (
                u'Erikoistehtävä',
                u'Mikäli olet sopinut erikseen työtehtävistä ja/tai sinut on ohjeistettu täyttämään lomake, '
                u'valitse tämä ja kerro tarkemmin Vapaa alue -kentässä mihin tehtävään ja kenen toimesta sinut '
                u'on valittu.',
                [tyovoima]
            ),
            (
                u'Info',
                u'Infopisteen henkilökunta vastaa kävijöiden kysymyksiin ja ratkaisee heidän ongelmiaan tapahtuman '
                u'aikana. Tehtävä edellyttää asiakaspalveluasennetta, tervettä järkeä ja ongelmanratkaisukykyä.',
                [tyovoima]
            ),
            (
                u'Järjestyksenvalvoja',
                u'Kävijöiden turvallisuuden valvominen conipaikalla ja yömajoituksessa. Edellyttää voimassa olevaa '
                u'JV-korttia ja asiakaspalveluasennetta. HUOM! Et voi valita tätä tehtävää hakemukseesi, ellet ole '
                u'täyttänyt tietoihisi JV-kortin numeroa (oikealta ylhäältä oma nimesi &gt; Pätevyydet).',
                [tyovoima]
            ),
            (
                u'Lipuntarkastaja',
                u'Lipuntarkastajana hoidat e-lippujen vaihtoa rannekkeiksi ja tarkistat lippuja ovella. Tehtävä '
                u'edellyttää asiakaspalveluasennetta.',
                [tyovoima]
            ),
            (
                u'Logistiikka', u'Autokuskina toimimista ja tavaroiden/ihmisten hakua ja noutamista. B-luokan '
                u'ajokortti vaaditaan. Työvuoroja myös perjantaille.',
                [tyovoima]
            ),
            (
                u'Narikka',
                u'Narikassa  säilytetään tapahtuman aikana kävijöiden omaisuutta. Tehtävä ei vaadi erikoisosaamista.',
                [tyovoima]
            ),
            (
                u'Pukuhuoneet',
                u'KUVAUS PUUTTUU',
                [tyovoima]
            ),
            (
                u'Salivänkäri',
                u'Luennoitsijoiden ja muiden ohjelmanpitäjien avustamista ohjelmanumeroiden yhteydessä.',
                [tyovoima]
            ),
            (
                u'Siivous',
                u'Siivousvänkärit ovat vastuussa tapahtuman yleisestä siisteydestä. He kulkevat ympäriinsä '
                u'tehtävänään roskakorien tyhjennys, vesipisteiden täyttö, vessoihin papereiden lisääminen '
                u'ja monet muut pienet askareet. Työ tehdään pääsääntöisesti vänkäripareittain.',
                [tyovoima]
            ),
            (
                u'Tekniikka',
                u'Salitekniikan (AV) ja tietotekniikan (tulostimet, lähiverkot, WLAN) nopeaa MacGyver-henkistä '
                u'ongelmanratkaisua.',
                [tyovoima]
            ),
            (
                u'Valokuvaus',
                u'Valokuvaus tapahtuu pääasiassa kuvaajien omilla järjestelmäkameroilla. Tehtäviä voivat olla '
                u'studiokuvaus, salikuvaus sekä yleinen valokuvaus. Kerro Työkokemus-kentässä aiemmasta '
                u'valokuvauskokemuksestasi (esim. linkkejä kuvagallerioihisi) sekä mitä/missä haluaisit '
                u'tapahtumassa valokuvata.',
                [tyovoima]
            ),
            (
                u'Yleisvänkäri',
                u'Sekalaisia tehtäviä laidasta laitaan, jotka eivät vaadi erikoisosaamista. Voit halutessasi '
                u'kirjata lisätietoihin, mitä osaat ja haluaisit tehdä.',
                [tyovoima]
            ),

            # (u'Kasaus ja purku', u'Kalusteiden siirtelyä & opasteiden kiinnittämistä. Ei vaadi erikoisosaamista. Työvuoroja myös jo pe sekä su conin sulkeuduttua, kerro lisätiedoissa jos voit osallistua näihin.', [tyovoima]),
            # (u'Majoitusvalvoja', u'Huolehtivat lattiamajoituspaikkojen pyörittämisestä yöaikaan. Työvuoroja myös molempina öinä.', [tyovoima]),
            # (u'Green room', u'Työvoiman ruokahuolto green roomissa. Edellyttää hygieniapassia.', [tyovoima]),
            # (u'Taltiointi', u'Taltioinnin keskeisiin tehtäviin kuuluvat mm. saleissa esitettävien ohjelmanumeroiden videointi tapahtumassa ja editointi tapahtuman jälkeen. Lisäksi videoidaan dokumentaarisella otteella myös yleisesti tapahtumaa. Kerro Työkokemus-kentässä aiemmasta videokuvauskokemuksestasi (esim. linkkejä videogallerioihisi) sekä mitä haluaisit taltioinnissa tehdä.', [tyovoima]),
        ]:
            if len(jc_data) == 3:
                name, description, pcs = jc_data
                job_names = []
            elif len(jc_data) == 4:
                name, description, pcs, job_names = jc_data
            else:
                raise ValueError("Length of jc_data must be 3 or 4")

            job_category, created = JobCategory.objects.get_or_create(
                event=self.event,
                slug=slugify(name),
                defaults=dict(
                    name=name,
                    description=description,
                )
            )

            if created:
                job_category.personnel_classes = pcs
                job_category.save()

            for job_name in job_names:
                job, created = Job.objects.get_or_create(
                    job_category=job_category,
                    slug=slugify(job_name),
                    defaults=dict(
                        title=job_name,
                    )
                )

        labour_event_meta.create_groups()

        for name in [u'Conitea']:
            JobCategory.objects.filter(event=self.event, name=name).update(public=False)

        for jc_name, qualification_name in [
            (u'Järjestyksenvalvoja', u'JV-kortti'),
            (u'Logistiikka', u'Henkilöauton ajokortti (B)'),
            # (u'Green room', u'Hygieniapassi'),
        ]:
            jc = JobCategory.objects.get(event=self.event, name=jc_name)
            qual = Qualification.objects.get(name=qualification_name)
            if not jc.required_qualifications.exists():
                jc.required_qualifications = [qual]
                jc.save()

        for diet_name in [
            u'Gluteeniton',
            u'Laktoositon',
            u'Maidoton',
            u'Vegaaninen',
            u'Lakto-ovo-vegetaarinen',
        ]:
            SpecialDiet.objects.get_or_create(name=diet_name)

        AlternativeSignupForm.objects.get_or_create(
            event=self.event,
            slug=u'conitea',
            defaults=dict(
                title=u'Conitean ilmoittautumislomake',
                signup_form_class_path='events.yukicon2016.forms:OrganizerSignupForm',
                signup_extra_form_class_path='events.yukicon2016.forms:OrganizerSignupExtraForm',
                active_from=datetime(2015, 11, 7, 12, 0, 0, tzinfo=self.tz),
                active_until=self.event.start_time,
            ),
        )

        for wiki_space, link_title, link_group in [
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


class Command(BaseCommand):
    args = ''
    help = 'Setup yukicon2016 specific stuff'

    option_list = BaseCommand.option_list + (
        make_option('--test',
            action='store_true',
            dest='test',
            default=False,
            help='Set the event up for testing',
        ),
    )

    def handle(self, *args, **opts):
        Setup().setup(test=opts['test'])
