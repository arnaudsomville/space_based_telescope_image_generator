"""Tracking Satellite, being the object used to capture images in orbit."""

import math
from vapory import POVRayElement, Camera

from space_based_telescope_image_generator.objects.target_object import TargetObject


class TrackingSatellite(POVRayElement):
    """Satellite being the main camera for image generation."""

    def __init__(self, position: list[float], fov: float = 60.0, image_width: int = 1920, image_height: int = 1080) -> None:
        """Constructor.

        Args:
            position (list[float]): Position vector in km.
        """
        self.position: list[float] = position
        self.pointing: list[float] = [0, 0, 0]  # NADIR pointing by default
        self.fov: float = fov
        self.image_width = image_width
        self.image_height = image_height

    def target_pointing(self, target_position: list[float]) -> list[float]:
        """Compute the Tracking Satellite's pointing.

        Args:
            target_position (list[float]): Position of the Target.

        Returns:
            list[float]: Pointing.
        """
        self.pointing = target_position
        return self.pointing

    def get_camera(self) -> Camera:
        """Return the camera object.

        Returns:
            Camera: Camera object representing the satellite.

        """
        return Camera(
            "location",
            self.position,
            "look_at",
            self.pointing,
            "angle",
            self.fov,
            "right",
            "x*image_width/image_height",
        )

    def compute_relative_distance(self, target: TargetObject) -> float:
        """Compute the distance with a target.

        Args:
            target (TargetObject): Target object.

        Returns:
            float: Distance in km.

        """
        return math.sqrt(
            (self.position[0] - target.position[0]) ** 2
            + (self.position[1] - target.position[1]) ** 2
            + (self.position[2] - target.position[2]) ** 2
        )
