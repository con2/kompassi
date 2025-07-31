from __future__ import annotations

from kompassi.dimensions.models.cached_dimensions import CachedDimensions
from kompassi.program_v2.models.cached_annotations import CachedAnnotations

from .base import BaseEmperkelator


class TraconEmperkelator(BaseEmperkelator):
    def get_dimensions(self) -> CachedDimensions:
        return super().get_dimensions()

    def get_annotations(self) -> CachedAnnotations:
        return super().get_annotations()
