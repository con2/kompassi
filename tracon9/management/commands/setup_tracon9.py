# encoding: utf-8

from datetime import datetime, timedelta

from django.conf import settings
from django.contrib.auth.models import Group
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand, make_option
from django.utils.timezone import get_default_timezone, now

from core.models import Event, Person, Venue
from labour.models import LabourEventMeta, JobCategory, Job, Qualification, WorkPeriod
from programme.models import ProgrammeEventMeta
from tickets.models import TicketsEventMeta, LimitGroup, Product

from ...models import SignupExtra, SpecialDiet, Night

class Command(BaseCommand):
    args = ''
    help = 'Setup tracon9 specific stuff'

    option_list = BaseCommand.option_list + (
        make_option('--test',
            action='store_true',
            dest='test',
            default=False,
            help='Set the event up for testing'
        ),
    )

    def handle(*args, **options):
        if options['test']:
            print 'Setting up tracon9 in test mode'
        else:
            print 'Setting up tracon9 in production mode'

        tz = get_default_timezone()

        venue, unused = Venue.objects.get_or_create(name='Tampere-talo')
        content_type = ContentType.objects.get_for_model(SignupExtra)
        event, unused = Event.objects.get_or_create(slug='tracon9', defaults=dict(
            name='Tracon 9',
            name_genitive='Tracon 9 -tapahtuman',
            name_illative='Tracon 9 -tapahtumaan',
            name_inessive='Tracon 9 -tapahtumassa',
            homepage_url='http://2014.tracon.fi',
            organization_name='Tracon ry',
            organization_url='http://ry.tracon.fi',
            start_time=datetime(2014, 9, 13, 10, 0, tzinfo=tz),
            end_time=datetime(2014, 9, 14, 18, 0, tzinfo=tz),
            venue=venue,
        ))

        labour_admin_group_name = "{installation_name}-{event_slug}-labour-admins".format(
            installation_name=settings.TURSKA_INSTALLATION_SLUG,
            event_slug=event.slug,
        )
        labour_admin_group, unused = Group.objects.get_or_create(name=labour_admin_group_name)

        if options['test']:
            person, unused = Person.get_or_create_dummy()
            labour_admin_group.user_set.add(person.user)

        labour_event_meta_defaults = dict(
            admin_group=labour_admin_group,
            signup_extra_content_type=content_type,
            work_begins=datetime(2014, 9, 12, 8, 0, tzinfo=tz),
            work_ends=datetime(2014, 9, 14, 22, 0, tzinfo=tz),
        )

        if options['test']:
            t = now()
            labour_event_meta_defaults.update(
                registration_opens=t - timedelta(days=60),
                registration_closes=t + timedelta(days=60),

            )
        else:
            labour_event_meta_defaults.update(
                registration_opens=datetime(2014, 3, 1, 0, 0, tzinfo=tz),
                registration_closes=datetime(2014, 8, 1, 0, 0, tzinfo=tz),
            )

        programme_admin_group_name = "{installation_name}-{event_slug}-programme-admins".format(
            installation_name=settings.TURSKA_INSTALLATION_SLUG,
            event_slug=event.slug,
        )
        programme_admin_group, unused = Group.objects.get_or_create(name=programme_admin_group_name)

        labour_event_meta, unused = LabourEventMeta.objects.get_or_create(event=event, defaults=labour_event_meta_defaults)
        programme_event_meta, unused = ProgrammeEventMeta.objects.get_or_create(event=event, defaults=dict(
            public=False,
            admin_group=programme_admin_group
        ))

        for name, description in [
            (u'Conitea', u'Tapahtuman järjestelytoimikunnan eli conitean jäsen'),
            (u'Erikoistehtävä', u'Mikäli olet sopinut erikseen työtehtävistä ja/tai sinut on ohjeistettu täyttämään lomake, valitse tämä ja kerro tarkemmin vapaa alue -kentässä mihin tehtävään ja kenen toimesta sinut on valittu.'),
            (u'Järjestyksenvalvoja', u'Kävijöiden turvallisuuden valvominen conipaikalla ja yömajoituksessa. Edellyttää voimassa olevaa JV-korttia ja asiakaspalveluasennetta.'),
            (u'Kasaus ja purku', u'Kalusteiden siirtelyä & opasteiden kiinnittämistä. Ei vaadi erikoisosaamista. Työvuoroja myös jo pe sekä su conin sulkeuduttua, kerro lisätiedoissa jos voit osallistua näihin.'),
            (u'Logistiikka', u'Autokuskina toimimista ja tavaroiden/ihmisten hakua ja noutamista. B-luokan ajokortti vaaditaan. Työvuoroja myös perjantaille.'),
            (u'Majoitusvalvoja', u'Huolehtivat lattiamajoituspaikkojen pyörittämisestä yöaikaan. Työvuoroja myös pe-la yölle.'),
            (u'Myynti', u'Pääsylippujen tai Tracon-oheistavaroiden myyntiä tai lippujen tarkastamista. Myyjiltä edellytetään täysi-ikäisyyttä, asiakaspalveluhenkeä ja huolellisuutta rahankäsittelyssä.'),
            (u'Narikka', u'Narikassa ja isotavara- eli asenarikassa säilytetään tapahtuman aikana kävijöiden omaisuutta. Tehtävä ei vaadi erityisempää erityisosaamista.'),
            (u'Ohjelma-avustaja', u'Lautapelien pyörittämistä, karaoken valvontaa, cosplay-kisaajien avustamista. Kerro vapaa alue -kohdassa tarkemmin, mitä haluaisit tehdä. Huom! Puheohjelmasalien vänkäreiltä toivotaan AV-tekniikan osaamista.'),
            (u'Ravitsemus ja virkistys', u'Työvoiman ruokahuolto Green Roomissa tai tapahtuman jälkeen kaatajaisissa. Hygieniapassi suositeltava.'),
            (u'Taltiointi', u'Taltioinnin keskeisiin tehtäviin kuuluvat mm. saleissa esitettävien ohjelmien taltiointi sekä jo tapahtuman aikana ja varsinkin tapahtuman jälkeen tallenteiden editointi. Lisäksi videoidaan dokumentaarisella otteella myös yleisesti tapahtumaa. Kerro lisätiedoissa aiemmasta videokuvaus kokemuksestasi (esim. linkkejä videogallerioihisi) sekä mitä haluaisit taltioinnissa tehdä.'),
            (u'Tekniikka', u'Salitekniikan (AV) ja tietotekniikan (tulostimet, lähiverkot, WLAN) nopeaa MacGyver-henkistä ongelmanratkaisua.'),
            (u'Valokuvaus', u'Valokuvaus tapahtuu pääasiassa kuvaajien omalla kalustolla, jota digitaalijärjestelmäkamerat edustavat. Tehtäviä voivat olla Kuvauspalvelu/Studiokuvaus, Salikuvaukset sekä yleinen valokuvaaminen. Kerro lisätiedoissa aiemmasta valokuvauskokemuksestasi (esim. linkkejä kuvagallerioihisi) sekä mitä/missä haluaisit tapahtumassa valokuvata.'),
            (u'Yleisvänkäri', u'Sekalaisia tehtäviä laidasta laitaan, jotka eivät vaadi erityisempää erityisosaamista. Voit halutessasi kirjata lisätietoihin, mitä osaat ja haluaisit tehdä.'),
        ]:
            JobCategory.objects.get_or_create(
                event=event,
                name=name,
                defaults=dict(
                    description=description
                )
            )

        for name in [u'Conitea', u'Erikoistehtävä']:
            JobCategory.objects.filter(event=event, name=name).update(public=False)

        jvkortti = Qualification.objects.get(name='JV-kortti')
        jv = JobCategory.objects.get(
            event=event,
            name=u'Järjestyksenvalvoja'
        )
        jv.required_qualifications = [jvkortti]
        jv.save()

        b_ajokortti = Qualification.objects.get(slug='b-ajokortti')
        logistiikka = JobCategory.objects.get(
            event=event,
            name=u'Logistiikka',
        )
        logistiikka.required_qualifications = [b_ajokortti]
        logistiikka.save()

        for job_category_name, job_names in [
            (u'Järjestyksenvalvoja', (
                u'Järjestyksenvalvojain vuoroesimies',
                u'Järjestyksenvalvoja',
            )),
            (u'Yleisvänkäri', (
                u'TS-1 -ryhmän ylivänkäri',
                u'TS-1 -ryhmän yleisvänkäri',
                u'TS-2 -ryhmän ylivänkäri',
                u'TS-2 -ryhmän yleisvänkäri',
            )),
        ]:
            job_category = JobCategory.objects.get(event=event, name=job_category_name)
            for job_name in job_names:
                Job.objects.get_or_create(job_category=job_category, title=job_name)

        period_length = timedelta(hours=8)
        for period_description, period_start in [
            ("Lauantain aamuvuoro", event.start_time.replace(hour=8)),
            ("Lauantain iltavuoro", event.start_time.replace(hour=16)),
            ("Lauantai-sunnuntai-yövuoro", event.end_time.replace(hour=0)),
            ("Sunnuntain aamuvuoro", event.end_time.replace(hour=8)),
        ]:
            WorkPeriod.objects.get_or_create(
                event=event,
                description=period_description,
                defaults=dict(
                    start_time=period_start,
                    end_time=period_start + period_length
                )
            )

        for diet_name in [
            u'Gluteeniton',
            u'Laktoositon',
            u'Maidoton',
            u'Vegaaninen',
        ]:
            SpecialDiet.objects.get_or_create(name=diet_name)

        for night in [
            u'Perjantain ja lauantain välinen yö',
            u'Lauantain ja sunnuntain välinen yö',
        ]:
            Night.objects.get_or_create(name=night)

        tickets_admin_group_name = "{installation_name}-{event_slug}-tickets-admins".format(
            installation_name=settings.TURSKA_INSTALLATION_SLUG,
            event_slug=event.slug,
        )
        tickets_admin_group, unused = Group.objects.get_or_create(name=tickets_admin_group_name)

        tickets_event_meta_defaults = dict(
            admin_group=tickets_admin_group,
            due_days=14,
            shipping_and_handling_cents=150,
            reference_number_template='9{:05d}',
        )

        if options['test']:
            t = now()
            tickets_event_meta_defaults.update(
                ticket_sales_starts=t - timedelta(days=60),
                ticket_sales_ends=t + timedelta(days=60),
            )
        else:
            tickets_event_meta_defaults.update(
                ticket_sales_starts=datetime(2014, 3, 1, 0, 0, tzinfo=tz),
                ticket_sales_ends=datetime(2014, 8, 31, 0, 0, tzinfo=tz),
            )

        tickets_meta, unused = TicketsEventMeta.objects.get_or_create(
            event=event,
            defaults=tickets_event_meta_defaults,
        )

        def limit_group(description, limit):
            limit_group, unused = LimitGroup.objects.get_or_create(
                event=event,
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
                name=u'Koko viikonlopun lippu (e-lippu)',
                description=u'Voimassa koko viikonlopun ajan la klo 10 - su klo 18. Toimitetaan sähköpostitse PDF-tiedostona.',
                limit_groups=[
                    limit_group('Lauantain liput', 5000),
                    limit_group('Sunnuntain liput', 5000),
                ],
                price_cents=1800,
                requires_shipping=False,
                available=True,
                ordering=ordering()
            ),

            dict(
                name=u'Lauantailippu (e-lippu)',
                description=u'Voimassa koko lauantaipäivän ajan la klo 10 - su klo 08. Toimitetaan sähköpostitse PDF-tiedostona.',
                limit_groups=[
                    limit_group('Lauantain liput', 5000),
                ],
                price_cents=1300,
                requires_shipping=False,
                available=True,
                ordering=ordering()
            ),

            dict(
                name=u'Sunnuntailippu (e-lippu)',
                description=u'Voimassa koko sunnuntai ajan su klo 00 - su klo 18. Toimitetaan sähköpostitse PDF-tiedostona.',
                limit_groups=[
                    limit_group('Sunnuntain liput', 5000),
                ],
                price_cents=1300,
                requires_shipping=False,
                available=True,
                ordering=ordering()
            ),

            dict(
                name=u'Koko viikonlopun lippu (postitse)',
                description=u'Voimassa koko viikonlopun ajan la klo 10 - su klo 18. Toimitetaan kirjeenä kotiisi.',
                limit_groups=[
                    limit_group('Lauantain liput', 5000),
                    limit_group('Sunnuntain liput', 5000),
                ],
                price_cents=1800,
                requires_shipping=True,
                available=True,
                ordering=ordering()
            ),

            dict(
                name=u'Lauantailippu (postitse)',
                description=u'Voimassa koko lauantaipäivän ajan la klo 10 - su klo 08. Toimitetaan kirjeenä kotiisi.',
                limit_groups=[
                    limit_group('Lauantain liput', 5000),
                ],
                price_cents=1300,
                requires_shipping=True,
                available=True,
                ordering=ordering()
            ),

            dict(
                name=u'Sunnuntailippu (postitse)',
                description=u'Voimassa koko sunnuntai ajan su klo 00 - su klo 18. Toimitetaan kirjeenä kotiisi.',
                limit_groups=[
                    limit_group('Sunnuntain liput', 5000),
                ],
                price_cents=1300,
                requires_shipping=True,
                available=True,
                ordering=ordering()
            ),

            dict(
                name=u'Lattiamajoitus pe-la (Aleksanterin koulu)',
                description=u'Lattiamajoituspaikka perjantain ja lauantain väliseksi yöksi Aleksanterin koululta.',
                limit_groups=[
                    limit_group('Lattiamajoitus pe-la, Aleksanterin koulu', 80),
                ],
                price_cents=1000,
                requires_shipping=False,
                available=True,
                ordering=ordering()
            ),

            dict(
                name=u'Lattiamajoitus la-su (Aleksanterin koulu)',
                description=u'Lattiamajoituspaikka lauantain ja sunnuntain väliseksi yöksi Aleksanterin koululta.',
                limit_groups=[
                    limit_group('Lattiamajoitus la-su, Aleksanterin koulu', 130),
                ],
                price_cents=1000,
                requires_shipping=False,
                available=True,
                ordering=ordering()
            ),

            dict(
                name=u'Lattiamajoitus la-su (Amurin koulu)',
                description=u'Lattiamajoituspaikka lauantain ja sunnuntain väliseksi yöksi Amurin koululta.',
                limit_groups=[
                    limit_group('Lattiamajoitus la-su, Amurin koulu', 250),
                ],
                price_cents=1000,
                requires_shipping=False,
                available=True,
                ordering=ordering()
            ),
        ]:
            name = product_info.pop('name')
            limit_groups = product_info.pop('limit_groups')
            product, unused = Product.objects.get_or_create(event=event, name=name, defaults=product_info)
            product.limit_groups = limit_groups
            product.save()
