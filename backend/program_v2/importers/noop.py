import logging

from django.db.models import QuerySet

from program_v2.models.dimension import Dimension
from program_v2.models.program import Program
from programme.models.programme import Programme

from .default import DefaultImporter

logger = logging.getLogger("kompassi")


class NoopImporter(DefaultImporter):
    """
    The NoopImporter is a subclass of the DefaultImporter that does nothing.
    You can use it to replace the importer of an old event whose program data
    should not be touched any more.

    Note that the NoopImporter will cowardly refuse to --dangerously-clear.
    """

    def import_dimensions(
        self,
        clear: bool = False,
        refresh_cached_dimensions: bool = True,
    ) -> list[Dimension]:
        if clear:
            raise RuntimeError("NoopImporter cowardly refuses to --dangerously-clear")

        logger.warning("NoopImporter asked to import dimensions – returning existing")
        return list(Dimension.objects.filter(event=self.event))

    def import_program(
        self,
        queryset: QuerySet[Programme],
        clear: bool = False,
        refresh_cached_fields: bool = True,
    ) -> list[Program]:
        if clear:
            raise RuntimeError("NoopImporter cowardly refuses to --dangerously-clear")

        logger.warning("NoopImporter asked to import program – doing nothing")
        return []
