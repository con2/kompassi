# encoding: utf-8

from datetime import datetime, timedelta

from django.contrib.auth.models import Group
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand, make_option
from django.utils.timezone import get_default_timezone, now

from core.models import Event, Person, Venue
from labour.models import LabourEventMeta, JobCategory, Job, Qualification, WorkPeriod
from programme.models import ProgrammeEventMeta

from ...models import SignupExtra, SpecialDiet

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

        labour_admin_group, unused = Group.objects.get_or_create(name='Tracon 9 -työvoimavastaavat')

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

        programme_admin_group, unused = Group.objects.get_or_create(name='Tracon 9 -ohjelmavastaavat')

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
            u'Laktoositon',
            u'Maidoton',
            u'Gluteeniton',
            u'Lakto-ovo-vegaaninen',
            u'Vegaaninen'
        ]:
            SpecialDiet.objects.get_or_create(name=diet_name)
