from django.utils.timezone import now

from ...models import ProgrammeEventMeta


class ColdOffersProgrammeEventMetaProxy(ProgrammeEventMeta):
    def publish(self):
        """
        Used by the start/stop signup period view to start the signup period. Returns True
        if the user needs to be warned about a certain corner case where information was lost.
        """
        warn = False

        if self.accepting_cold_offers_until and self.accepting_cold_offers_until <= now():
            self.accepting_cold_offers_until = None
            warn = True

        self.accepting_cold_offers_from = now()
        self.save()

        return warn

    def unpublish(self):
        self.accepting_cold_offers_until = now()
        self.save()

    @property
    def is_public(self):
        return self.is_accepting_cold_offers

    class Meta:
        proxy = True
