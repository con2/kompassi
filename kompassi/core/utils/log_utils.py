import logging


def log_get_or_create(logger: logging.Logger, obj, created: bool):
    level = logging.INFO if created else logging.DEBUG
    logger.log(
        level,
        "{kind} {name} {what_done}".format(
            kind=obj.__class__.__name__,
            name=str(obj),
            what_done="created" if created else "already exists",
        ),
    )


def log_delete(
    logger: logging.Logger,
    delete_result: tuple[int, dict[str, int]],
    *,
    zero_level: int | None = logging.INFO,
    nonzero_level: int | None = logging.INFO,
    message: str = "Objects deleted",
    **extra: object,
):
    total_deleted, deleted_by_model = delete_result

    level = zero_level if total_deleted == 0 else nonzero_level
    if level is None:
        return

    logger.log(
        level,
        message,
        extra=dict(
            total=total_deleted,
            by_model=deleted_by_model,
            **extra,
        ),
    )
