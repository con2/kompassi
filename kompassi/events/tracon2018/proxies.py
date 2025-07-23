from dateutil.tz import tzlocal

from kompassi.core.csv_export import CsvExportMixin

from .models import SignupExtra


class SignupExtraAfterpartyProxy(SignupExtra, CsvExportMixin):
    class Meta:
        proxy = True

    @property
    def personnel_class_name(self):
        from kompassi.badges.models import Badge

        badge, unused = Badge.ensure(event=self.event, person=self.person)
        return badge.personnel_class.name if badge else ""

    @property
    def afterparty_signup_time_local(self):
        from kompassi.labour.models import SurveyRecord

        try:
            record = SurveyRecord.objects.get(
                survey__event__slug="tracon2018",
                survey__slug="kaatoilmo",
                person=self.person,
            )
            return record.created_at.astimezone(tzlocal()).replace(tzinfo=None)
        except SurveyRecord.DoesNotExist:
            return None

    @classmethod
    def get_csv_fields(cls, event):
        from kompassi.core.models import Person

        return [
            (cls, "afterparty_signup_time_local"),
            (cls, "personnel_class_name"),
            (Person, "surname"),
            (Person, "first_name"),
            (Person, "nick"),
            (Person, "email"),
            (Person, "normalized_phone_number"),
            (cls, "outward_coach_departure_time"),
            (cls, "return_coach_departure_time"),
            (cls, "formatted_special_diet"),
            (cls, "special_diet_other"),
            (cls, "willing_to_bartend"),
            # TODO FIX THIS IN csv_export
            (cls, next(f for f in cls._meta.many_to_many if f.name == "pick_your_poison")),
        ]

    def get_csv_related(self):
        from kompassi.core.models import Person

        return {
            Person: self.person,
        }
