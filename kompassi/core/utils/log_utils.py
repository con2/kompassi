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


def log_delete(logger: logging.Logger, delete_result: tuple[int, dict[str, int]]):
    total_deleted, deleted_by_model = delete_result
    logger.info(
        "Deleted %s objects (%s)",
        total_deleted,
        ", ".join(f"{k}: {v}" for k, v in deleted_by_model.items()),
    )
