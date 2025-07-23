import logging

from kompassi.core.utils import get_previous_and_next
from kompassi.core.utils.pkg_resources_compat import resource_string

from ...models import Programme

logger = logging.getLogger(__name__)


class ProgrammeManagementProxy(Programme):
    """
    Contains extra methods for Programme used only by management views.
    """

    def get_overlapping_programmes(self):
        if any(
            (
                self.id is None,
                self.room is None,
                self.start_time is None,
                self.length is None,
            )
        ):
            return ProgrammeManagementProxy.objects.none()
        else:
            return ProgrammeManagementProxy.objects.raw(
                resource_string(__name__, "sql/overlapping_programmes.sql").decode(),
                (
                    self.category.event.id,
                    self.id,
                    self.room.id,
                    self.start_time,
                    self.end_time,
                ),
            )

    def get_previous_and_next_programme(self):
        queryset = ProgrammeManagementProxy.objects.filter(category__event=self.category.event).order_by("title")
        return get_previous_and_next(queryset, self)

    class Meta:
        proxy = True
