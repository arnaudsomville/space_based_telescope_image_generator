"""Target object."""

from vapory import Texture, Pigment, Finish, Box, Union, POVRayElement

class TargetObject(POVRayElement):
    """Base for targets."""

    def __init__(self, position: list[float], rotation: list[float])->None:
        """_summary_

        Args:
            position (list[float]): Position vector in km.
            rotation (list[float]): Rotation vector of the object in degree.

        """
        super().__init__()
        self.position = position
        self.rotation = rotation

    def get_position(self)->list[float]:
        """Retrieve object's position.

        Returns:
            list[float]: Position.
        """
        return self.position

    def get_rotation(self)->list[float]:
        """Retrieve object's rotation.

        Returns:
            list[float]: rotation.
        """
        return self.rotation
