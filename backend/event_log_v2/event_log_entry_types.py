from .registry import register

register(
    name="event_log_v2.entry.partition_created",
    message="Event log partition created: {partition_name}",
)

register(
    name="event_log_v2.entry.partition_deleted",
    message="Event log partition deleted: {partition_name}",
)
