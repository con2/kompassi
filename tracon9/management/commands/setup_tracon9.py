# encoding: utf-8

from datetime import datetime, timedelta

from django.core.management.base import BaseCommand, make_option
from django.contrib.contenttypes.models import ContentType
from django.utils.timezone import get_default_timezone, now

from core.models import Event, Venue
from labour.models import LabourEventMeta, JobCategory, Qualification
from ...models import SignupExtra

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
        tz = get_default_timezone()

        venue, unused = Venue.objects.get_or_create(name='Tampere-talo')
        content_type = ContentType.objects.get_for_model(SignupExtra)
        event, unused = Event.objects.get_or_create(slug='tracon9', defaults=dict(
            name='Tracon 9',
            name_genitive='Tracon 9 -tapahtuman',
            homepage_url='http://2014.tracon.fi',
            organization_name='Tracon ry',
            organization_url='http://ry.tracon.fi',
            venue=venue
        ))

        tz = get_default_timezone()

        if options['test']:
            t = now()
            event_meta_defaults = dict(
                signup_extra_content_type=content_type,
                registration_opens=t - timedelta(days=60),
                registration_closes=t + timedelta(days=60)
            )
        else:
            event_meta_defaults = dict(
                signup_extra_content_type=content_type,
                registration_opens=datetime(2014, 3, 1, 0, 0, tzinfo=tz),
                registration_closes=datetime(2014, 8, 1, 0, 0, tzinfo=tz)
            )

        event_meta, unused = LabourEventMeta.objects.get_or_create(event=event, defaults=event_meta_defaults)

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
