"""Base class to define astral objects like planets, moons, stars..."""

from vapory import (
    POVRayElement,
)

from abc import ABC, abstractmethod


class AstralObject(ABC, POVRayElement):
    """Base class for all the astral objects."""

    def __init__(self, additional_includes: list[str] = []):
        """Create inherited attributes."""
        self.additional_includes = additional_includes

    @abstractmethod
    def get_povray_object(self):
        """Retrieve the povray object."""
        pass
