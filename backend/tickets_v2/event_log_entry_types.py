from event_log_v2 import registry

registry.register(
    name="tickets_v2.order.viewed",
    message="Order {order_number} in {event} was viewed by {actor}",
)

registry.register(
    name="tickets_v2.order.created",
    message="Order {order_number} in {event} was administratively created by {actor}",
)

registry.register(
    name="tickets_v2.order.cancelled",
    message="Order {order_number} in {event} was cancelled by {actor_type} {actor}",
)

registry.register(
    name="tickets_v2.order.refunded.provider",
    message="Order {order_number} in {event} was provider refunded by {actor_type} {actor}",
)

registry.register(
    name="tickets_v2.order.refunded.manual",
    message="Order {order_number} in {event} was manually marked as refunded by {actor_type} {actor}",
)

registry.register(
    name="tickets_v2.order.marked_as_paid",
    message="Order {order_number} in {event} was manually marked as paid by {actor_type} {actor}",
)
