from dataclasses import dataclass

from core.models import Event, Person


@dataclass
class FormsEventMeta:
    """
    No need for an actual model for now. This serves as a stand-in for GraphQL.
    """

    event: Event


@dataclass
class FormsProfileMeta:
    """
    No need for an actual model for now. This serves as a stand-in for GraphQL.
    """

    person: Person
