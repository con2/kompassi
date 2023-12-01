from dataclasses import dataclass

from core.models import Event


@dataclass
class FormsEventMeta:
    """
    No need for an actual model for now. This serves as a stand-in for GraphQL.
    """

    event: Event
