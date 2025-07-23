import logging

from dateutil.tz import tzlocal
from paikkala.models import Ticket

from kompassi.core.csv_export import CsvExportMixin

from .models import SignupExtra

logger = logging.getLogger(__name__)


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
                survey__event__slug="tracon2023",
                survey__slug="kaatoilmo",
                person=self.person,
            )
            return record.created_at.astimezone(tzlocal()).replace(tzinfo=None)
        except SurveyRecord.DoesNotExist:
            return None

    def get_coach_by_programme_title(self, title):
        from kompassi.zombies.programme.models import Programme

        try:
            programme = Programme.objects.get(category__event=self.event, title=title)
        except Programme.DoesNotExist:
            logger.exception("Programme %r not found", title)
            return None

        try:
            ticket = programme.paikkala_program.tickets.get(user=self.person.user)
        except Ticket.DoesNotExist:
            # ENOBUS
            return None

        return ticket.zone.name

    @property
    def outward_coach(self):
        return self.get_coach_by_programme_title("Kaatobussin paikkavaraus, menomatka")

    @property
    def return_coach(self):
        return self.get_coach_by_programme_title("Kaatobussin paikkavaraus, paluumatka")

    @classmethod
    def get_csv_fields(cls, event):
        assert event.slug == "tracon2023"
        from kompassi.core.models import Person

        return [
            (cls, "afterparty_signup_time_local"),
            (cls, "personnel_class_name"),
            (Person, "surname"),
            (Person, "first_name"),
            (Person, "nick"),
            (Person, "email"),
            (Person, "normalized_phone_number"),
            (cls, "outward_coach"),
            (cls, "return_coach"),
            (cls, "formatted_special_diet"),
            (cls, "special_diet_other"),
            (cls, "afterparty_help"),
            # TODO FIX THIS IN csv_export
            (cls, next(f for f in cls._meta.many_to_many if f.name == "pick_your_poison")),
        ]

    def get_csv_related(self):
        from kompassi.core.models import Person

        return {
            Person: self.person,
        }
