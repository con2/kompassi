# encoding: utf-8

from django.forms import ValidationError
from django.test import TestCase

from jsonschema import ValidationError

from core.models import Person
from badges.models import BadgesEventMeta
from programme.models import ProgrammeEventMeta, Programme

from .models import Desuprofile
from .utils import import_programme


class DesuprofileValidationTestCase(TestCase):
    def test_idempotence(self):
        valid_profile = dict(
            id=2559,
            username='japsu',
            email='foo@bar.fi', # required
            first_name='Foo',
            last_name='Bar',
            nickname='Quux',
            phone='',
            birth_date='2014-04-24',
        )

        self.assertEqual(Desuprofile.from_dict(valid_profile)._asdict(), valid_profile)

    def test_desuprofile_without_required_attributes(self):
        blank_email = dict(
            id=2559,
            username='japsu',
            email='', # required
            first_name='Foo',
            last_name='Bar',
            nickname='Quux',
            phone='',
            birth_date='2014-04-24',
        )

        with self.assertRaises(ValidationError):
            Desuprofile.from_dict(blank_email)

        missing_first_name = dict(
            id=2559,
            username='japsu',
            email='foo@bar.fi',
            # first_name='Foo',
            last_name='Bar',
            nickname='Quux',
            phone='',
            birth_date='2014-04-24',
        )

        with self.assertRaises(ValidationError):
            Desuprofile.from_dict(missing_first_name)

    def test_invalid_values(self):
        malformed_birth_date = dict(
            id=2559,
            username='japsu',
            email='foo@bar.fi',
            first_name='Foo',
            last_name='Bar',
            nickname='Quux',
            phone='',
            birth_date='2014-04b-24',
        )

        with self.assertRaises(ValidationError):
            Desuprofile.from_dict(malformed_birth_date)

        malformed_email = dict(
            id=2559,
            username='japsu',
            email='look no at sign.fi',
            first_name='Foo',
            last_name='Bar',
            nickname='Quux',
            phone='',
            birth_date='2014-04-24',
        )

        with self.assertRaises(ValidationError):
            Desuprofile.from_dict(malformed_email)

    def test_quirks(self):
        # Desuprofile gives null instead of missing key or empty string for birth_date
        null_birth_date = dict(
            id=2559,
            username='japsu',
            email='foo@bar.fi',
            first_name='Foo',
            last_name='Bar',
            nickname='Quux',
            phone='',
            birth_date=None,
        )

        Desuprofile.from_dict(null_birth_date)



class DesuprogrammeImportTestCase(TestCase):
    def setUp(self):
        self.meta, unused = BadgesEventMeta.get_or_create_dummy()
        ProgrammeEventMeta.get_or_create_dummy()

        self.event = self.meta.event
        self.person, unused = Person.get_or_create_dummy()

    def test_programme_import(self):
        payload = [
            dict(
                identifier='katsot-animea-vaarin',
                title='Katsot animea väärin',
                description='Niidel vertaa syksyn 2011 DesuTalksissa Helsingin Glorialla animeharrastusta parisuhteeseen, osoittaa kriittisimmät virheet juuri sinun.',
            ),
            dict(
                identifier='todellisuusopas-komeroille',
                title='Todellisuusopas komeroille',
                description='Oletko kyllästynyt valittamaan laudoilla kuinka haluaisit vain paijata? Olisiko vihdoinkin aika tulla ulos komerosta? Tämä itsensäkehittämisluento yrittää auttaa juuri sinua joka olet suunnittelemassa todellisuudelle avautumista. Opit mitä sinun tulisi tietää todellisuudesta ja saat vinkkejä sinne siirtymiseen. Tai jos olet vielä epävarma ulostautumisestasi, saat tietää mitä todellisuudella on tarjota ja syitä vaivautumiseen. Todellisuusopas painottuu parisuhteisiin, ja antaa sinulle konkreettisen kaavan jolla nörtti saa tyttö-/poikaystävän. Luentoa värittävät havainnot animen ja todellisuuden eroavaisuuksista ja mahdollisista yhtäläisyyksistä. Kaikki nämä elintärkeät tiedonjyvät esitetään nautinnollisen helpostisulatettavalla, humoristisella tavalla.',
            ),
        ]

        assert Programme.objects.all().count() == 0

        import_programme(self.event, payload)

        assert Programme.objects.all().count() == 2
        assert Programme.objects.filter(state='accepted').count() == 2

        # Now cancel the latter
        import_programme(self.event, payload[:1])

        assert Programme.objects.all().count() == 2
        assert Programme.objects.filter(state='accepted').count() == 1
        assert Programme.objects.filter(state='cancelled').count() == 1

        # Reinstate it
        import_programme(self.event, payload)

        assert Programme.objects.all().count() == 2
        assert Programme.objects.filter(state='accepted').count() == 2
        assert Programme.objects.filter(state='cancelled').count() == 0

        # Change something
        programme = Programme.objects.get(slug='todellisuusopas-komeroille')
        assert programme.title == 'Todellisuusopas komeroille'
        payload[1]['title'] = 'Todellisuusopas komeroille 2.0'
        import_programme(self.event, payload)
        programme = Programme.objects.get(slug='todellisuusopas-komeroille')
        assert programme.title == 'Todellisuusopas komeroille 2.0'
