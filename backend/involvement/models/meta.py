from dataclasses import dataclass

from core.models.event import Event

from .invitation import Invitation


@dataclass
class InvolvementEventMeta:
    """
    No need for an actual model for now. This serves as a stand-in for GraphQL.
    """

    event: Event

    @property
    def invitations(self):
        return Invitation.objects.filter(
            survey__event=self.event,
        ).select_related(
            "survey",
            "program",
        )
