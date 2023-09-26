def log_get_or_create(logger, obj, created):
    logger.info(
        "{kind} {name} {what_done}".format(
            kind=obj.__class__.__name__,
            name=str(obj),
            what_done="created" if created else "already exists",
        )
    )


def log_delete(logger, delete_result: tuple[int, dict[str, int]]):
    total_deleted, deleted_by_model = delete_result
    logger.info(
        "Deleted %s objects (%s)",
        total_deleted,
        ", ".join(f"{k}: {v}" for k, v in deleted_by_model.items()),
    )
