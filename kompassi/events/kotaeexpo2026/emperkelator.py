from kompassi.dimensions.models.cached_annotations import CachedAnnotations
from kompassi.involvement.emperkelators.base import BaseEmperkelator
from kompassi.involvement.models.enums import InvolvementType


class KotaeEmperkelator(BaseEmperkelator):
    def get_annotation_values(self) -> CachedAnnotations:
        has_varakettu_signup = any(
            involvement.type == InvolvementType.LEGACY_SIGNUP and involvement.title.casefold() == "varakettu"
            for involvement in self.involvements
        )
        if has_varakettu_signup:
            return {"internal:overrideFormattedPerks": "ÄLÄ ANNA BADGEA"}

        return super().get_annotation_values()
