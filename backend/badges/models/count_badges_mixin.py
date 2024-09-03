from dataclasses import dataclass
from itertools import cycle

from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from .constants import BADGE_ELIGIBLE_FOR_BATCHING, PROGRESS_ELEMENT_MIN_WIDTH


@dataclass
class Progress:
    css_class: str
    max: int
    text: str
    value: int
    width: int
    inflated: bool


class CountBadgesMixin:
    def count_printed_badges(self) -> int:
        return (
            self.badges.filter(
                Q(batch__isnull=False, batch__printed_at__isnull=False) | Q(printed_separately_at__isnull=False)
            )
            .distinct()
            .count()
        )

    def count_badges_waiting_in_batch(self) -> int:
        return self.badges.filter(batch__isnull=False, batch__printed_at__isnull=True, revoked_at__isnull=True).count()

    def count_badges_awaiting_batch(self) -> int:
        return self.badges.filter(**BADGE_ELIGIBLE_FOR_BATCHING).count()

    def count_badges(self) -> int:
        return self.badges.count()

    def count_revoked_badges(self) -> int:
        return self.badges.filter(revoked_at__isnull=False).count()

    def get_progress(self):
        """
        We build a progress bar widget that shows percentages of badges in different states.
        However, if the percentage is really small, the progress segment in the progress bar
        would get too small. We account for that by "inflating" segments that are too small,
        and "deflating" segments that are big enough so that taking away some of their width
        does not cause a signicifant error in their relative sizes.

        TODO: This method should be generalized to work with all kinds of multi-segment
        progress bars, not just this particular occasion.
        """
        progress = []

        pb_max = self.count_badges()
        percentace_consumed_for_inflation = 0

        for pb_class, pb_text, pb_value in [
            ("progress-bar-success", _("Printed"), self.count_printed_badges()),
            ("progress-bar-danger", _("Revoked"), self.count_revoked_badges()),
            ("progress-bar-info", _("Waiting in batch"), self.count_badges_waiting_in_batch()),
            ("progress-bar-grey", _("Awaiting allocation into batch"), self.count_badges_awaiting_batch()),
        ]:
            if pb_value > 0:
                width = 100.0 * pb_value / max(pb_max, 1)
                width = int(width + 0.5)

                if width < PROGRESS_ELEMENT_MIN_WIDTH:
                    percentace_consumed_for_inflation += PROGRESS_ELEMENT_MIN_WIDTH - width
                    width = PROGRESS_ELEMENT_MIN_WIDTH
                    inflated = True
                else:
                    inflated = False

                progress.append(
                    Progress(
                        css_class=pb_class,
                        max=pb_max,
                        text=pb_text,
                        value=pb_value,
                        width=width,
                        inflated=inflated,
                    )
                )

        if sum(p.width for p in progress) > 100:
            candidates_for_deflation = [p for p in progress if p.width > PROGRESS_ELEMENT_MIN_WIDTH]
            candidates_for_deflation.sort(key=lambda p: -p.width)

            for p in cycle(candidates_for_deflation):
                if sum(p.width for p in progress) <= 100 or all(
                    p.width <= PROGRESS_ELEMENT_MIN_WIDTH for p in candidates_for_deflation
                ):
                    break

                if p.width > PROGRESS_ELEMENT_MIN_WIDTH:
                    p.width -= 1
                    percentace_consumed_for_inflation -= 1

        # FIXME sometime this assert blows
        # assert sum(p.width for p in progress) in [100, 0], "Missing percentage"

        return progress
