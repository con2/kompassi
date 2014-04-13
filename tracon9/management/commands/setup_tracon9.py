# encoding: utf-8

from datetime import datetime, timedelta

from django.conf import settings
from django.contrib.auth.models import Group
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand, make_option
from django.utils.timezone import now

from dateutil.tz import tzlocal

from core.utils import give_all_app_perms_to_group
from core.models import Event, Person, Venue
from labour.models import LabourEventMeta, JobCategory, Job, Qualification, WorkPeriod
from programme.models import ProgrammeEventMeta, Category, Programme, Room, Role
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

        tz = tzlocal()

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

        labour_accepted_group, unused = LabourEventMeta.get_or_create_group(event, 'accepted')
        labour_applicants_group, unused = LabourEventMeta.get_or_create_group(event, 'applicants')
        labour_admin_group, unused = LabourEventMeta.get_or_create_group(event, 'admins')
        give_all_app_perms_to_group('labour', labour_admin_group)

        if options['test']:
            person, unused = Person.get_or_create_dummy()
            labour_admin_group.user_set.add(person.user)

        labour_event_meta_defaults = dict(
            admin_group=labour_admin_group,
            accepted_group=labour_accepted_group,
            applicants_group=labour_applicants_group,
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

        programme_admin_group, unused = ProgrammeEventMeta.get_or_create_group(event, 'admins')
        give_all_app_perms_to_group('programme', programme_admin_group)

        labour_event_meta, unused = LabourEventMeta.objects.get_or_create(event=event, defaults=labour_event_meta_defaults)
        programme_event_meta, unused = ProgrammeEventMeta.objects.get_or_create(event=event, defaults=dict(
            public=False,
            admin_group=programme_admin_group
        ))

        room_order = 0
        for room_name in [
            'Iso sali',
            'Pieni sali',
            'Sopraano',
            'Rondo',
            'Studio',
            'Sonaatti 1',
            'Sonaatti 2',
            'Basso',
            'Opus 1',
            'Opus 2',
            'Opus 3',
            'Opus 4',
            'Ulkona (teltta)',
        ]:
            room_order += 100
            Room.objects.get_or_create(
                venue=venue,
                name=room_name,
                defaults=dict(
                    order=room_order
                )
            )

        # v5
        if not programme_event_meta.contact_email:
            programme_event_meta.contact_email = 'ohjelma@tracon.fi'
            programme_event_meta.save()

        role, unused = Role.objects.get_or_create(
            title=u'Ohjelmanjärjestäjä',
            defaults=dict(
                is_default=True,
                require_contact_info=True,
            )
        )

        # v8
        role.is_default = True
        role.save()

        for title, style in [
            (u'Animeohjelma', u'anime'),
            (u'Cosplayohjelma', u'cosplay'),
            (u'Miitti', u'miitti'),
            (u'Muu ohjelma', u'muu'),
            (u'Roolipeliohjelma', u'rope'),
        ]:
            Category.objects.get_or_create(
                event=event,
                style=style,
                defaults=dict(
                    title=title,
                )
            )

        if options['test']:
            # create some test programme
            Programme.objects.get_or_create(
                category=Category.objects.get(title='Animeohjelma', event=event),
                title='Yaoi-paneeli',
                defaults=dict(
                    description='Kika-kika tirsk',
                )
            )

        for name, description in [
            (u'Conitea', u'Tapahtuman järjestelytoimikunnan eli conitean jäsen'),
            (u'Erikoistehtävä', u'Mikäli olet sopinut erikseen työtehtävistä ja/tai sinut on ohjeistettu täyttämään lomake, valitse tämä ja kerro tarkemmin Vapaa alue -kentässä mihin tehtävään ja kenen toimesta sinut on valittu.'),
            (u'Järjestyksenvalvoja', u'Kävijöiden turvallisuuden valvominen conipaikalla ja yömajoituksessa. Edellyttää voimassa olevaa JV-korttia ja asiakaspalveluasennetta.'),
            (u'Ensiapu', 'Toimit osana tapahtuman omaa ensiapuryhmää. Vuoroja päivisin ja öisin tapahtuman aukioloaikoina. Vaaditaan vähintään voimassa oleva EA1 -kortti ja osalta myös voimassa oleva EA2 -kortti. Kerro Työkokemus -kohdassa osaamisestasi, esim. oletko toiminut EA-tehtävissä tapahtumissa tai oletko sairaanhoitaja/lähihoitaja koulutuksestaltasi.'),
            (u'Kasaus ja purku', u'Kalusteiden siirtelyä & opasteiden kiinnittämistä. Ei vaadi erikoisosaamista. Työvuoroja myös jo pe sekä su conin sulkeuduttua, kerro lisätiedoissa jos voit osallistua näihin.'),
            (u'Logistiikka', u'Autokuskina toimimista ja tavaroiden/ihmisten hakua ja noutamista. B-luokan ajokortti vaaditaan. Työvuoroja myös perjantaille.'),
            (u'Majoitusvalvoja', u'Huolehtivat lattiamajoituspaikkojen pyörittämisestä yöaikaan. Työvuoroja myös molempina öinä.'),
            (u'Myynti', u'Pääsylippujen ja Tracon-oheistuotteiden myyntiä sekä lippujen tarkastamista. Myyjiltä edellytetään täysi-ikäisyyttä, asiakaspalveluhenkeä ja huolellisuutta rahankäsittelyssä. Vuoroja myös perjantaina.'),
            (u'Narikka', u'Narikassa ja isotavara- eli asenarikassa säilytetään tapahtuman aikana kävijöiden omaisuutta. Tehtävä ei vaadi erikoisosaamista.'),
            (u'Ohjelma-avustaja', u'Lautapelien pyörittämistä, karaoken valvontaa, cosplay-kisaajien avustamista. Kerro Vapaa alue -kohdassa tarkemmin, mitä haluaisit tehdä. Huom! Puheohjelmasalien vänkäreiltä toivotaan AV-tekniikan osaamista.'),
            (u'Green room', u'Työvoiman ruokahuolto green roomissa. Hygieniapassi suositeltava.'),
            (u'Taltiointi', u'Taltioinnin keskeisiin tehtäviin kuuluvat mm. saleissa esitettävien ohjelmanumeroiden videointi tapahtumassa ja editointi tapahtuman jälkeen. Lisäksi videoidaan dokumentaarisella otteella myös yleisesti tapahtumaa. Kerro Työkokemus-kentässä aiemmasta videokuvauskokemuksestasi (esim. linkkejä videogallerioihisi) sekä mitä haluaisit taltioinnissa tehdä.'),
            (u'Tekniikka', u'Salitekniikan (AV) ja tietotekniikan (tulostimet, lähiverkot, WLAN) nopeaa MacGyver-henkistä ongelmanratkaisua.'),
            (u'Valokuvaus', u'Valokuvaus tapahtuu pääasiassa kuvaajien omilla järjestelmäkameroilla. Tehtäviä voivat olla studiokuvaus, salikuvaus sekä yleinen valokuvaus. Kerro Työkokemus-kentässä aiemmasta valokuvauskokemuksestasi (esim. linkkejä kuvagallerioihisi) sekä mitä/missä haluaisit tapahtumassa valokuvata.'),
            (u'Yleisvänkäri', u'Sekalaisia tehtäviä laidasta laitaan, jotka eivät vaadi erikoisosaamista. Voit halutessasi kirjata lisätietoihin, mitä osaat ja haluaisit tehdä.'),
        ]:
            JobCategory.objects.get_or_create(
                event=event,
                name=name,
                defaults=dict(
                    description=description
                )
            )

        for name in [u'Conitea']:
            JobCategory.objects.filter(event=event, name=name).update(public=False)

        jvkortti = Qualification.objects.get(name='JV-kortti')
        jv = JobCategory.objects.get(
            event=event,
            name=u'Järjestyksenvalvoja'
        )
        if not jv.required_qualifications.exists():
            jv.required_qualifications = [jvkortti]
            jv.save()

        b_ajokortti = Qualification.objects.get(slug='b-ajokortti')
        logistiikka = JobCategory.objects.get(
            event=event,
            name=u'Logistiikka',
        )
        if not logistiikka.required_qualifications.exists():
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
            if not job_category.job_set.exists():
                for job_name in job_names:
                    Job.objects.get_or_create(job_category=job_category, title=job_name)

        period_length = timedelta(hours=8)
        for period_description, period_start in [
            ("Lauantain aamuvuoro (la klo 08-16)", event.start_time.replace(hour=8)),
            ("Lauantain iltavuoro (la klo 16-24)", event.start_time.replace(hour=16)),
            ("Lauantai-sunnuntai-yövuoro (su klo 00-08)", event.end_time.replace(hour=0)),
            ("Sunnuntain aamuvuoro (su klo 08-16)", event.end_time.replace(hour=8)),
            ("Sunnuntain iltavuoro (su klo 16-20)", event.end_time.replace(hour=16)),
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
            u'Lakto-ovo-vegaaninen',
        ]:
            SpecialDiet.objects.get_or_create(name=diet_name)

        for night in [
            u'Perjantain ja lauantain välinen yö',
            u'Lauantain ja sunnuntain välinen yö',
        ]:
            Night.objects.get_or_create(name=night)

        tickets_admin_group, unused = TicketsEventMeta.get_or_create_group(event, 'admins')
        give_all_app_perms_to_group('tickets', tickets_admin_group)

        tickets_event_meta_defaults = dict(
            admin_group=tickets_admin_group,
            due_days=14,
            shipping_and_handling_cents=100,
            reference_number_template='9{:05d}',
            contact_email='Tracon 9 -lipunmyynti <liput@tracon.fi>',
            plain_contact_email='liput@tracon.fi',
            ticket_spam_email='japsu@tracon.fi',
            ticket_free_text=u"Tämä on sähköinen lippusi Tracon 9 -tapahtumaan. Sähköinen lippu vaihdetaan rannekkeeseen\n"
                u"lipunvaihtopisteessä saapuessasi tapahtumaan. Voit tulostaa tämän lipun tai näyttää sen\n"
                u"älypuhelimen tai tablettitietokoneen näytöltä. Mikäli kumpikaan näistä ei ole mahdollista, ota ylös\n"
                u"kunkin viivakoodin alla oleva neljästä tai viidestä sanasta koostuva sanakoodi ja ilmoita se\n"
                u"lipunvaihtopisteessä.\n\n"
                u"Tervetuloa Traconiin!"
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
                description=u'Voimassa koko viikonlopun ajan la klo 10 - su klo 18. Toimitetaan sähköpostitse PDF-tiedostona. Ei toimituskuluja.',
                limit_groups=[
                    limit_group('Lauantain liput', 5000),
                    limit_group('Sunnuntain liput', 5000),
                ],
                price_cents=1800,
                requires_shipping=False,
                electronic_ticket=True,
                available=True,
                ordering=ordering()
            ),

            dict(
                name=u'Koko viikonlopun lippu (postitse)',
                description=u'Voimassa koko viikonlopun ajan la klo 10 - su klo 18. Toimitetaan kirjeenä kotiisi. Toimituskulut 1,00 €/tilaus.',
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
                name=u'Lauantailippu (e-lippu)',
                description=u'Voimassa koko lauantaipäivän ajan la klo 10 - su klo 08. Toimitetaan sähköpostitse PDF-tiedostona. Ei toimituskuluja.',
                limit_groups=[
                    limit_group('Lauantain liput', 5000),
                ],
                price_cents=1200,
                requires_shipping=False,
                electronic_ticket=True,
                available=True,
                ordering=ordering()
            ),

            dict(
                name=u'Lauantailippu (postitse)',
                description=u'Voimassa koko lauantaipäivän ajan la klo 10 - su klo 08. Toimitetaan kirjeenä kotiisi. Toimituskulut 1,00 €/tilaus.',
                limit_groups=[
                    limit_group('Lauantain liput', 5000),
                ],
                price_cents=1200,
                requires_shipping=True,
                available=True,
                ordering=ordering()
            ),

            dict(
                name=u'Sunnuntailippu (e-lippu)',
                description=u'Voimassa koko sunnuntai ajan su klo 00 - su klo 18. Toimitetaan sähköpostitse PDF-tiedostona. Ei toimituskuluja.',
                limit_groups=[
                    limit_group('Sunnuntain liput', 5000),
                ],
                price_cents=1000,
                requires_shipping=False,
                electronic_ticket=True,
                available=True,
                ordering=ordering()
            ),

            dict(
                name=u'Sunnuntailippu (postitse)',
                description=u'Voimassa koko sunnuntai ajan su klo 00 - su klo 18. Toimitetaan kirjeenä kotiisi. Toimituskulut 1,00 €/tilaus.',
                limit_groups=[
                    limit_group('Sunnuntain liput', 5000),
                ],
                price_cents=1000,
                requires_shipping=True,
                available=True,
                ordering=ordering()
            ),

            dict(
                name=u'Lattiamajoitus 2 yötä pe-su (Aleksanterin koulu)',
                description=u'Lattiamajoituspaikka pe-la ja la-su välisiksi öiksi Aleksanterin koululta. Majoituspaikasta ei tule erillistä lippua, vaan majoitus toimii nimilistaperiaatteella. Majoituspaikoista ei aiheudu toimituskuluja. Saat lisäohjeita majoituksesta sähköpostiisi ennen tapahtumaa.',
                limit_groups=[
                    limit_group('Lattiamajoitus pe-la, Aleksanterin koulu', 80),
                    limit_group('Lattiamajoitus la-su, Aleksanterin koulu', 130),
                ],
                price_cents=2000,
                requires_shipping=False,
                available=True,
                ordering=ordering()
            ),

            dict(
                name=u'Lattiamajoitus 1 yö la-su (Amurin koulu)',
                description=u'Lattiamajoituspaikka lauantain ja sunnuntain väliseksi yöksi Amurin koululta. Majoituspaikasta ei tule erillistä lippua, vaan majoitus toimii nimilistaperiaatteella. Majoituspaikoista ei aiheudu toimituskuluja. Saat lisäohjeita majoituksesta sähköpostiisi ennen tapahtumaa.',
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
            if not product.limit_groups.exists():
                product.limit_groups = limit_groups
                product.save()
