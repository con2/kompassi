import logging
import os
from datetime import datetime, timedelta

from dateutil.tz import tzlocal
from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils.timezone import now



from kompassi.core.models import Event





logger = logging.getLogger(__name__)




class Setup:

    def setup(self, test=False):
        self.test = test
        self.tz = tzlocal()


        self.setup_core()# Tapahtuma info


        self.setup_labour()# Vänkärit ja Vastaavat // hakulomake
        self.setup_intra() # Perähallinta käyttäjä ryhmät



        self.setup_program_v2()# Ohjelma databaasi merkintä



    def setup_core(self):
        from kompassi.core.models import Organization, Venue

        self.venue, _ = Venue.objects.get_or_create(
            name="Turun yliopisto",
            defaults=dict(
                name_inessive="Turun yliopistolla",
            ),
        )

        self.organization, _ = Organization.objects.get_or_create(
            slug="Finncon-yhdistys ry",
            defaults=dict(
                name="Finncon-yhdistys ry",
                homepage_url="http://www.finncon.org/",
            ),
        )

        self.event, _ = Event.objects.get_or_create(
            slug="finncon2026",
            defaults=dict(
                name="Finncon 2026",
                name_genitive="Finncon 2026 -tapahtuman",
                name_illative="Finncon 2026 -tapahtumaan",
                name_inessive="Finncon 2026 -tapahtumassa",
                homepage_url="http://2026.finncon.org",
                organization=self.organization,
                start_time=datetime(2026, 7, 10, 10, 0, tzinfo=self.tz),
                end_time=datetime(2026, 7, 12, 18, 0, tzinfo=self.tz),
                venue=self.venue,
            ),
        )









    def setup_labour(self):
        from django.contrib.contenttypes.models import ContentType
        from kompassi.core.models import Person
        from kompassi.labour.models import LabourEventMeta, Qualification
        from kompassi.labour.models.personnel_class import PersonnelClass
        from kompassi.labour.models.job_category import JobCategory

        from ...models import SignupExtra, SpecialDiet
        from kompassi.labour.models import (
            AlternativeSignupForm,
            InfoLink,
            JobCategory,
            LabourEventMeta,
            PersonnelClass,
            Qualification,
        )


        (labour_admin_group,) = LabourEventMeta.get_or_create_groups(self.event, ["admins"])
        content_type = ContentType.objects.get_for_model(SignupExtra)


        labour_event_meta_defaults = dict(
            signup_extra_content_type=content_type,
            work_begins=self.event.start_time.replace(hour=8), #Starts at 8:
            work_ends=self.event.start_time.replace(hour=22), #Ends at 22:
            registration_opens=datetime(2026, 2, 10, 0, 0, tzinfo=self.tz),
            registration_closes=datetime(2026, 6, 20, 0, 0, tzinfo=self.tz), #arbitary
            admin_group=labour_admin_group,
            contact_email="Finnconin työvoimavastaava <tyovoima@2026.finncon.org>",
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



        for diet_name in ["Gluteeniton", "Laktoositon", "Maidoton", "Vegaaninen", "Lakto-ovo-vegetaristinen"]:
            SpecialDiet.objects.get_or_create(name=diet_name)






        ## organizers -- vastaavat PersonnelClass
        organizers_personnel_class, created = PersonnelClass.objects.get_or_create(
            event=self.event,
            slug="vastaava",
            defaults=dict(
                name="Vastaavat",
                app_label="labour",
                priority=10,
            ),
        )


        ## Vapaaehtoinen työkategoria
        volunteer_pc, _ = PersonnelClass.objects.get_or_create(
            event=self.event,
            slug="vapaaehtoinen",
            defaults=dict(
                name="Vapaaehtoinen",
                app_label="labour",
                priority=30,
            ),
        )



        ## Vapaaehtoinen työkategoria
#        voluntary_gategory, v_created = JobCategory.objects.update_or_create(
#            event=self.event,
#            slug="vapaaehtoinen",
#            defaults=dict(
#                name="Vänkäri (Vapaaehtoinen)",
#                description="Tapahtuman vapaaehtoistehtävät eri osa-alueilla.",
#                public=True,
#            ),
#        )
#        if v_created:
#            voluntary_gategory.personnel_classes.set([volunteer_pc])


        for slug, name, description in [
            ("vankari", "Yleisvänkäri", "Valmiina auttamaan siellä, missä tarvitaan. Yleisvänkärille hyviä ominaisuuksia ovat esim. oma-aloitteisuus. Yleisvänkäreitä sijoitetaan tapahtuman aikana eri puolille conia ja toiveita oman sijoittumisen suhteen saa esittää. Yleisvänkärille voi tulla myös päivystysvuoro Vänkäriluolassa, jolloin siellä huolehditaan samalla tarjoilujen ylläpidosta ja tilan siisteydestä, sekä lähdetään tarvittaessa sinne missä apua kaivataan."),
            ("vankarigreen", "Taukotilavänkäri", "Löytyykö sinulta hygieniapassi, ruokapuolen osaamista tai intoa oppia näitä taitoja? Haluatko olla varmistamassa, että henkilökunta pysyy virkeänä ja hyvin ravittuna con-päivän ajan? Hae osaksi taukotilatiimiä, joka huolehtii tapahtuman aikana Greenroomin, Vänkäriluolan ja näytteilleasetajien taukopaikan kahvi- ja välipalatatjoiluista, sekä näiden tilojen siisteydestä, kasauksesta ja purusta. Hygieniapassi ei ole pakollinen, mutta yleinen osaaminen ymmärrys elintarviketurvallisuudesta ja esimerkiksi hyvästä käsihygieniasta on. Muita hyviä ominaisuuksia tehtävään ovat omatoimisuus, järjestelmällisyys ja toimeliaisuus, sekä sosiaaliset taidot vuorovaikutettaessa niin taukotilaan levähtämään tulevan henkilökunnan kuin oman tiiminkin kanssa."),
            ("vankariinfo", "Infovänkäri", "Omaatko hyvät vuorovaikutustaidot ja “ellen tiedä niin ei hätää, minä selvitän!” -asenteen? Hae osaksi Finnconin tuikitärkeää infotiimiä huolehtimaan, että niin kävijät kuin henkilökuntakin pysyvät informoituina ja löytävät oikeaan aikaan tiensä perille. Info kokoaa myös sinne tuodut löytötavarat ja luovuttaa ne kyselijöille tavaran tuntomerkkejä vastaan."),
            ("vankarinarikka", "Narikkavänkäri", "Narikassa autat varmistamaan, että kävijöiden isommat kantamukset pysyvät turvassa tapahtuman ajan. Selkeä tehtävä, jossa pärjää omatessaan hyvät vuorovaikutustaidot, sekä ripauksen käytännöllistä loogisuutta."),
            ("vankaripurku", "Purku-/rakennusvänkäri", "Haluatko nauttia itse tapahtumasta rauhassa ja antaa työpanoksesi ennen sen alkua ja/tai tapahtuman päätyttyä? Tule osaksi kasaus- ja purkutiimiä! Hommiin sisältyy monenmoista roudailua, joten kohtuullinen fyysinen kunto ja ergonomiset työtavat ovat tässä tehtävässä paikallaan."),
            ("vankariohjelma", "Ohjelmavänkäri", "Haluaisitko toimia ohjelmapitäjien apuna luentosalissa tai työpajassa? Tehtävässä hyödyksi ovat avulias asenne(jos esimerkiksi pöytiä tai tuoleja pitää järjestää uudelleen tai yleisön kysyjälle viedä mikrofoni), salivänkärillä tekninen osaaminen. Pajavänkäreillä myös käsityöharrastuneisuus voi olla eduksi työpajojen vetäjiä autettaessa."),
            ("tiiminvetaja", "Tiiminvetäjä", "Finncon on iso tapahtuma ja vapaaehtoisia yleensä paljon. Tehtävien jaon helpottamiseksi haussa on myös tiiminvetäjiä toimimaan oman vastuualueensa vänkäreiden tukena tapahtuman aikana yhteistyössä työvoimavastaavan kanssa. Tehtävässä keskeisiä taitoja ovat hyvät vuorovaikutustaidot ja ongelmaratkaisukyky, järjestelmällisyys, aktiivinen ote hommiin ja itsenäinen päätöksentekokyky."),
        ]:
            jc, created = JobCategory.objects.update_or_create(
                event=self.event,
                slug=slug,
                defaults=dict(
                    name=name,
                    app_label="vapaaehtoinen",
                    description=description,
                    public=True,
                ),
            )
            if created:
                jc.personnel_classes.set([volunteer_pc])




        ## Finncon 2026 työryhmä JobCategory
        conitea_job_category, created = JobCategory.objects.update_or_create(
            event=self.event,
            slug="conitea",
            defaults=dict(
                name="Finncon 2026 conitea",
                description="Tapahtuman suunnittelusta ja valmistelusta vastaavan järjestelytyöryhmän jäsen",
                public=False,
            ),
        )

        if created:
            conitea_job_category.personnel_classes.set([organizers_personnel_class])




        ## taika koodi??? ## Vaatii aiemman iteraation
#        for jc_name, qualification_name in [
#            ("Järjestyksenvalvoja", "JV-kortti"),
#        ]:
#            JobCategory.objects.get(event=self.event, name=jc_name)
#            Qualification.objects.get(name=qualification_name)

        valvoja, j_created = JobCategory.objects.update_or_create(
            event=self.event,
            slug="valvoja",
            defaults=dict(
                name="Järjestyksenvalvoja",
                description='JV-kortti taskussa? Tehtävässä vaaditaan hyviä vuorovaikutustaitoja ja tilannetajua, sekä rauhallisen jämäkkää otetta. Jos et tällä hetkellä omista JV-korttia ja olet sen suorittamassa sen koulutuksen ennen tapahtumaa, mainitse asiasta "Vapaa alue" tekstikentässä!',
                public=True,
            ),
        )

        if j_created:
            valvoja.personnel_classes.set([volunteer_pc])
            qual = Qualification.objects.get(name="JV-kortti")
            valvoja.required_qualifications.set([qual])






        AlternativeSignupForm.objects.get_or_create(
            event=self.event,
            slug="conitea",
            defaults=dict(
                title="Conitean ilmoittautumislomake",
                signup_form_class_path="events.finncon2026.forms:OrganizerSignupForm",
                signup_extra_form_class_path="events.finncon2026.forms:OrganizerSignupExtraForm",
                active_from=now(),
                active_until=self.event.start_time,
            ),
        )



        labour_event_meta.create_groups() ## Pitää kutsua luonnin jälkeen





    def setup_intra(self):
        from kompassi.intra.models import IntraEventMeta

        (admin_group,) = IntraEventMeta.get_or_create_groups(self.event, ["admins"])
        organizer_group = self.event.labour_event_meta.get_group("vastaava")
        IntraEventMeta.objects.update_or_create(
            event=self.event,
            defaults=dict(
                admin_group=admin_group,
                organizer_group=organizer_group,
            ),
        )




    def setup_program_v2(self):
        from kompassi.involvement.models.registry import Registry
        from kompassi.program_v2.models.meta import ProgramV2EventMeta


        ## Vänkäri rekisteri
        registry, _created = Registry.objects.get_or_create(
            scope=self.organization.scope,
            slug="volunteers",
            defaults=dict(
                title_fi="Finncon 2026 vapaaehtoisrekisteri",
                title_en="Volunteers of Finncon2026",
            ),
        )


        (admin_group,) = ProgramV2EventMeta.get_or_create_groups(self.event, ["admins"])
        meta, _ = ProgramV2EventMeta.objects.update_or_create(
            event=self.event,
            defaults=dict(
                admin_group=admin_group,
                guide_v2_embedded_url="https://2026.finncon.org/ohjelma/",
                contact_email="Finncon 2026 ohjelmatiimi <ohjelma@2026.finncon.org>",
                default_registry=Registry.objects.get(
                    scope=self.event.organization.scope,
                    slug="volunteers",
                ),
            ),
        )
        meta.ensure()




class Command(BaseCommand):
    args = ""
    help = "Setup finncon2026 specific stuff"

    def handle(self, *args, **opts):
        Setup().setup(test=settings.DEBUG)
