"""Base class to define astral objects like planets, moons, stars..."""

from vapory import (
    POVRayElement,
)

from abc import ABC, abstractmethod

class AstralObject(ABC, POVRayElement):
    """Base class for all the astral objects."""

    @abstractmethod
    def get_povray_object(self):
        """Retrieve the povray object."""
        pass

