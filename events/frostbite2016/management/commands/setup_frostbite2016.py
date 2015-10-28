# encoding: utf-8

from datetime import datetime, timedelta

from django.core.management.base import BaseCommand, make_option
from django.utils.timezone import now

from dateutil.tz import tzlocal

from core.utils import slugify
from pytz import timezone


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
        self.setup_labour()
        self.setup_access()

    def setup_core(self):
        from core.models import Venue, Event

        self.venue, unused = Venue.objects.get_or_create(name='Lahden Sibeliustalo', defaults=dict(
            name_inessive='Lahden Sibeliustalolla',  # not really inessive though
        ))
        self.event, unused = Event.objects.get_or_create(slug='frostbite2016', defaults=dict(
            name='Desucon Frostbite 2016',
            name_genitive='Desucon Frostbite 2016 -tapahtuman',
            name_illative='Desucon Frostbite 2016 -tapahtumaan',
            name_inessive='Desucon Frostbite 2016 -tapahtumassa',
            homepage_url='https://desucon.fi/frostbite2016/',
            organization_name='Kehittyvien conien Suomi ry',
            organization_url='https://desucon.fi/kcs/',
            start_time=datetime(2016, 1, 15, 17, 0, 0, tzinfo=timezone('Europe/Helsinki')),
            end_time=datetime(2016, 1, 17, 17, 0, 0, tzinfo=timezone('Europe/Helsinki')),
            venue=self.venue,
        ))

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
        from ...models import SignupExtra
        from django.contrib.contenttypes.models import ContentType

        labour_admin_group, created = LabourEventMeta.get_or_create_group(self.event, 'admins')

        if self.test and created:
            from core.models import Person
            person, unused = Person.get_or_create_dummy()
            labour_admin_group.user_set.add(person.user)

        content_type = ContentType.objects.get_for_model(SignupExtra)

        labour_event_meta_defaults = dict(
            signup_extra_content_type=content_type,
            work_begins=datetime(2016, 1, 15, 6, 0, tzinfo=self.tz),
            work_ends=datetime(2016, 1, 17, 21, 0, tzinfo=self.tz),
            registration_opens=datetime(2015, 9, 21, 18, 0, tzinfo=self.tz),
            registration_closes=datetime(2015, 1, 4, 23, 59, 59, tzinfo=self.tz),
            admin_group=labour_admin_group,
            contact_email='Frostbite 2016 -työvoimavastaava <tyovoima@desucon.fi>',
        )

        if self.test:
            t = now()
            labour_event_meta_defaults.update(
                registration_opens=t - timedelta(days=60),
                registration_closes=t + timedelta(days=60),
            )

        labour_event_meta, unused = LabourEventMeta.objects.get_or_create(
            event=self.event,
            defaults=labour_event_meta_defaults,
        )

        for pc_name, pc_slug, pc_app_label in [
            (u'Vastaava', 'vastaava', 'labour'),
            (u'Vuorovastaava', 'ylivankari', 'labour'),
            (u'Työvoima', 'tyovoima', 'labour'),
            (u'Ohjelmanjärjestäjä', 'ohjelma', 'programme'),
            (u'Guest of Honour', 'goh', 'programme'),
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
        vastaava = PersonnelClass.objects.get(event=self.event, slug='vastaava')
        ylivankari = PersonnelClass.objects.get(event=self.event, slug='ylivankari')
        ohjelma = PersonnelClass.objects.get(event=self.event, slug='ohjelma')

        for name, description, pcs in [
            (u'Vastaava', u'Tapahtuman vastaava', [vastaava]),
            (u'Pelisali', u'', [tyovoima, ylivankari]),
            (u'Meido', u'', [tyovoima, ylivankari]),
            (u'Sidosryhmät', u'', [tyovoima, ylivankari]),
            (u'AV-tekniikka', u'', [tyovoima, ylivankari]),
            (u'DesuTV', u'', [tyovoima, ylivankari]),
            (u'Tulkki', u'', [tyovoima, ylivankari]),

            (u'Narikka', u'Narikkavänkärit ovat vastuussa tapahtuman narikoiden pyörittämisestä. Työ itsessään on yksinkertaista, mutta tekemistä sen sijaan on varmasti riittävästi. Narikkavänkärit ovat määrällisesti suurin vänkäriryhmä.', [tyovoima, ylivankari]),
            (u'Siivous', u'Siivousvänkärit ovat vastuussa tapahtuman yleisestä siisteydestä. He kulkevat ympäriinsä tehtävänään roskakorien tyhjennys, vesipisteiden täyttö, vessoihin papereiden lisääminen ja monet muut pienet askareet. Työ tehdään pääsääntöisesti vänkäripareittain.', [tyovoima, ylivankari]),
            (u'Green Room', u'GreenRoom -vänkärinä sinun täytyy olla kykeneväinen itsenäiseen ja oma-aloitteeseen työskentelyyn. Tehtäviisi kuuluu kahvin keitto, esivalmistelutyöt, paikkojen siistiminen ym. Huomioithan että tekemistä riittää GreenRoomissa lähestulkoon läpi vuorokauden, joten tämä ei ole pesti jossa pärjää peukkujen pyörittelyllä.', [tyovoima, ylivankari]),
            (u'Info', u'Infotiski on tapahtuman hyvin öljytty hermokeskus, joka ottaa vastaan ja ohjaa informaatiota eteenpäin. Työnkuvaasi infotiskillä kuuluu kysymyksiin vastaaminen niin kävijöille kuin työvoimallekin, neuvonta, kuulutukset ja muun informaation edelleenlähetys asianomaisille. Infopiste on yksi tapahtumapaikan näkyvimmistä työvoimapisteistä. Sen työntekijöiltä toivotaan asiakaspalveluosaamista ja ongelmanratkaisutaitoja sekä hyvää huumorintajua.', [tyovoima, ylivankari]),
            (u'Järjestyksenvalvoja', u'Kävijöiden turvallisuuden valvominen conipaikalla. Edellyttää voimassa olevaa JV-korttia ja asiakaspalveluasennetta. HUOM! Et voi valita tätä tehtävää hakemukseesi, ellet ole täyttänyt tietoihisi JV-kortin numeroa (oikealta ylhäältä oma nimesi > Pätevyydet).', [tyovoima, ylivankari]),
            (u'Valokuvaaja', u'Desukuvaajana tehtävänäsi on yleis-, ohjelma- ja photoshoot-kuvaus. Kuvauspisteen kuvaajat kuvaavat cosplayasuja studiossa. Valokuvaus tapahtuu kuvaajien omalla kalustolla.', [tyovoima, ylivankari]),
            (u'Taltiointi', u'Taltiointivänkärit tallentavat Desuconin ohjelmista äänen ja kuvan. Osa taltiointitiimin jäsenistä myös editoi tämän materiaalin, jotta ohjelmat ovat nähtävissä myöhemminkin. Lisäksi taltiointivänkärit kuvaavat videomateriaalia muuten tapahtumasta.', [tyovoima, ylivankari]),
            (u'Myyntisali', u'Myyntisalivänkärin tehtävänä on pääsääntöisesti vastata Desuconin oman oheistuotemyyntipöydän tuotteiden järjestelemisestä ja myymisestä. Myyntisalivänkärin toimenkuvaan kuuluu myös myyntisalissa päivystäminen: tämä tarkoittaa kävijöiden kysymyksiin vastaamista, ohjeistamista, myyjien Green Roomin ylläpitoa ja myyjien auttamista ongelmatilanteissa. Hakijoilta vaaditaan aiempaa rahankäsittelykokemusta.', [tyovoima, ylivankari]),
            (u'Lipunmyynti', u'Lipunmyyntivänkärin tehtävänä on lukea kävijöiden lippuvarmenteita ja antaa heille rannekkeita. Tässä pestissä ei välttämättä tule minimi työvaatimus täyteen, joten lipunmyyntivänkäri saattaa löytää itsensä tekemästä jännittäviä yllätystehtäviä.', [tyovoima, ylivankari]),
            (u'Tekniikka', u'Tekniikkavänkärit huolehtivat tapahtuman aikana teknologian toimivuudesta. Työtehtävät ovat hyvin monipuolisia jatkojohtojen toimittamisesta ohjelmansalien äänentoistosta huolehtimiseen, joten tietotekniikan laaja perustuntemus on valinnan edellytyksenä.', [tyovoima, ylivankari]),
            (u'Cosplay', u'Cosplayvänkäreiden tehtävänä on huolehtia etupäässä cosplaykisaajien avustamisesta harjoitusten ja kilpailujen aikana takahuoneessa ja kulisseissa. Työ jakautuu kaikille conipäiville ja sisältää moninaista puuhaa kisaajien ohjaamisesta paikkalippujen jakamiseen ja lavasteiden kuljettamiseen.', [tyovoima, ylivankari]),
            (u'Majoitus', u'Majoitusvänkärin tehtävä on vastata majoittujien turvallisuudesta. Vänkärit ottavat majoittujat vastaan, ja pitävät huolta siitä, että ketään ylimääräistä ei päästetä majoitustiloihin. Vänkärit myös kiertelevät majoitustiloja ympäri valvomassa järjestystä. Työ tehdään lattiamajoitusalueella.', [tyovoima, ylivankari]),

            (u'Ohjelmanpitäjä', u'Luennon tai muun vaativan ohjelmanumeron pitäjä', [ohjelma]),
        ]:
            job_category, created = JobCategory.objects.get_or_create(
                event=self.event,
                name=name,
                defaults=dict(
                    description=description,
                    slug=slugify(name),
                )
            )

            if created:
                job_category.personnel_classes = pcs
                job_category.save()

        labour_event_meta.create_groups()

        # for name in [u'Vastaava', u'Pelisali', u'Meido', u'Sidosryhmät', u'AV-tekniikka', u'DesuTV', u'Tulkki', ]:
        #     JobCategory.objects.filter(event=self.event, name=name).update(public=False)

        for jc_name, qualification_name in [
            (u'Järjestyksenvalvoja', u'JV-kortti'),
        ]:
            jc = JobCategory.objects.get(event=self.event, name=jc_name)
            qual = Qualification.objects.get(name=qualification_name)

            jc.required_qualifications = [qual]
            jc.save()

        organizer_form, unused = AlternativeSignupForm.objects.get_or_create(
            event=self.event,
            slug=u'vastaava',
            defaults=dict(
                title=u'Vastaavan ilmoittautumislomake',
                signup_form_class_path='events.frostbite2016.forms:OrganizerSignupForm',
                signup_extra_form_class_path='events.frostbite2016.forms:OrganizerSignupExtraForm',
                active_from=datetime(2015, 8, 18, 0, 0, 0, tzinfo=self.tz),
                active_until=self.event.start_time,
            ),
        )

        if organizer_form.active_until is None:
            organizer_form.active_until = self.event.start_time
            organizer_form.save()

        AlternativeSignupForm.objects.get_or_create(
            event=self.event,
            slug=u'xxlomake',
            defaults=dict(
                title=u'Jälki-ilmoittautumislomake',
                signup_form_class_path='events.frostbite2016.forms:LatecomerSignupForm',
                signup_extra_form_class_path='events.frostbite2016.forms:LatecomerSignupExtraForm',
                active_from=datetime(2015, 8, 18, 0, 0, 0, tzinfo=self.tz),
                active_until=self.event.start_time,
                signup_message=u'Yleinen työvoimahaku Desucon Frostbiteen ei ole enää auki. Täytä tämä lomake vain, '
                    u'jos joku Desuconin vastaavista on ohjeistanut sinun ilmoittautua tällä lomakkeella. ',
            ),
        )

    def setup_access(self):
        from access.models import Privilege, GroupPrivilege

        # Grant accepted workers access to Tracon Slack
        group = self.event.labour_event_meta.get_group('accepted')
        privilege = Privilege.objects.get(slug='desuslack')
        GroupPrivilege.objects.get_or_create(group=group, privilege=privilege, defaults=dict(event=self.event))


class Command(BaseCommand):
    args = ''
    help = 'Setup frostbite2016 specific stuff'

    option_list = BaseCommand.option_list + (
        make_option(
            '--test',
            action='store_true',
            dest='test',
            default=False,
            help='Set the event up for testing',
        ),
    )

    def handle(self, *args, **opts):
        Setup().setup(test=opts['test'])
