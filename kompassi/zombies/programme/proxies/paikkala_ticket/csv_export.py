from paikkala.models import Ticket

from kompassi.core.csv_export import CsvExportMixin


class PaikkalaTicketCsvExportProxy(CsvExportMixin, Ticket):
    class Meta:
        proxy = True

    @classmethod
    def get_csv_fields(cls, event):
        from kompassi.core.models import Person

        return [
            (cls, "zone"),
            (cls, "row"),
            (cls, "number"),
            (Person, "surname"),
            (Person, "first_name"),
            (Person, "nick"),
            (Person, "normalized_phone_number"),
            (Person, "email"),
        ]

    @property
    def zone(self):
        return super().zone.name

    @property
    def row(self):
        return super().row.name

    def get_csv_related(self):
        from kompassi.core.models import Person

        return {
            Person: self.user.person,
        }
