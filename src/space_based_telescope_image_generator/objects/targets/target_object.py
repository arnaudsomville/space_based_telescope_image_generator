"""Target object."""

from vapory import POVRayElement

from abc import ABC, abstractmethod


class TargetObject(ABC, POVRayElement):
    """Base for targets."""

    def __init__(
        self,
        position: list[float],
        attitude: list[float],
        additional_includes: list[str] = [],
    ) -> None:
        """_summary_

        Args:
            position (list[float]): Position vector in km.
            rotation (list[float]): Rotation vector of the object in degree.
            additional_includes: list[str]: Important includes.

        """
        super().__init__()
        self.position = position
        self.attitude = attitude
        self.additional_includes = additional_includes

    def get_position(self) -> list[float]:
        """Retrieve object's position.

        Returns:
            list[float]: Position.
        """
        return self.position

    def get_attitude(self) -> list[float]:
        """Retrieve object's attitude.

        Returns:
            list[float]: attitude.
        """
        return self.attitude

    @abstractmethod
    def get_povray_object(self):
        """Retrieve the povray object."""
        pass
