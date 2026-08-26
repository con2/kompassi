from contextlib import contextmanager

from graphql import GraphQLError

from ..models.order import OrderStateChanged, TicketsUnavailable

# Machine-readable codes for the order state machine's refusals. The frontend branches
# on these (via extensions.code) instead of matching the exception's English message.
ORDER_STATE_CHANGED = "ORDER_STATE_CHANGED"
TICKETS_UNAVAILABLE = "TICKETS_UNAVAILABLE"


@contextmanager
def order_errors_as_graphql_errors():
    """
    Re-raises the exceptions Order.fulfil() and Order.cancel_and_refund() use to refuse
    an operation as GraphQLErrors carrying extensions.code. graphql-core copies the
    extensions onto the error it wraps a resolver exception in, and graphene-django
    serialises them via GraphQLError.formatted, so the code reaches the client.

    The message is preserved verbatim: it is what the admin UI shows if it does not
    recognise the code.
    """
    try:
        yield
    except OrderStateChanged as e:
        raise GraphQLError(str(e), extensions={"code": ORDER_STATE_CHANGED}) from e
    except TicketsUnavailable as e:
        raise GraphQLError(str(e), extensions={"code": TICKETS_UNAVAILABLE}) from e
