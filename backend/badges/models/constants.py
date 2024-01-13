BADGE_ELIGIBLE_FOR_BATCHING = dict(
    batch__isnull=True,
    printed_separately_at__isnull=True,
    revoked_at__isnull=True,
)

PROGRESS_ELEMENT_MIN_WIDTH = 4  # %
