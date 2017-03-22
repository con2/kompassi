# encoding: utf-8



from django.db import models

from dateutil.tz import tzlocal

from core.csv_export import CsvExportMixin

from .models import SignupExtraV2


class SignupExtraV2AfterpartyProxy(SignupExtraV2, CsvExportMixin):
    class Meta:
        proxy = True

    @property
    def personnel_class_name(self):
        from badges.models import Badge
        badge, unused = Badge.ensure(event=self.event, person=self.person)
        return badge.personnel_class.name if badge else ''

    @property
    def afterparty_signup_time_local(self):
        from labour.models import SurveyRecord

        try:
            record = SurveyRecord.objects.get(
                survey__event__slug='tracon11',
                survey__slug='kaatoilmo',
                person=self.person,
            )
            return record.created_at.astimezone(tzlocal()).replace(tzinfo=None)
        except SurveyRecord.DoesNotExist:
            return None

    @classmethod
    def get_csv_fields(cls, event):
        assert event.slug == 'tracon11'
        from core.models import Person
        from labour.models import PersonnelClass

        return [
            (cls, 'afterparty_signup_time_local'),
            (cls, 'personnel_class_name'),
            (Person, 'surname'),
            (Person, 'first_name'),
            (Person, 'nick'),
            (Person, 'email'),
            (Person, 'phone'),
            (cls, 'outward_coach_departure_time'),
            (cls, 'return_coach_departure_time'),
            (cls, 'formatted_special_diet'),
            (cls, 'special_diet_other'),
        ]

    def get_csv_related(self):
        from core.models import Person

        return {
            Person: self.person,
        }
