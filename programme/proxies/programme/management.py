from pkg_resources import resource_string
import logging

from core.utils import (
    get_postgresql_version_num,
    get_previous_and_next,
)

from ...models import Programme


HAVE_POSTGRESQL_TIME_RANGE_FUNCTIONS = get_postgresql_version_num() >= 90200
logger = logging.getLogger('kompassi')


class ProgrammeManagementProxy(Programme):
    """
    Contains extra methods for Programme used only by management views.
    """

    def get_overlapping_programmes(self):
        if any((
            self.id is None,
            self.room is None,
            self.start_time is None,
            self.length is None,
        )):
            return ProgrammeManagementProxy.objects.none()
        elif HAVE_POSTGRESQL_TIME_RANGE_FUNCTIONS:
            return ProgrammeManagementProxy.objects.raw(
                resource_string(__name__, 'sql/overlapping_programmes.sql'),
                (
                    self.category.event.id,
                    self.id,
                    self.room.id,
                    self.start_time,
                    self.end_time,
                )
            )
        else:
            logger.warn('DB engine not PostgreSQL >= 9.2. Cannot detect overlapping programmes.')
            return ProgrammeManagementProxy.objects.none()

    def get_previous_and_next_programme(self):
        queryset = ProgrammeManagementProxy.objects.filter(category__event=self.category.event).order_by('title')
        return get_previous_and_next(queryset, self)

    class Meta:
        proxy = True