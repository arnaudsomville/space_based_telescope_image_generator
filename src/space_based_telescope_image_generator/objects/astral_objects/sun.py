"""Definition of Sun lightsource."""

from vapory import LightSource
from space_based_telescope_image_generator.objects.astral_objects.astral_object import (
    AstralObject,
)
from space_based_telescope_image_generator.utils.constants import OBLIQUITY, earth_sun_distance
import math as m
import datetime



class Sun(AstralObject):
    """Definition of sun being the lightsource.

    Args:
        AstralObject (_type_): _description_
    """

    def __init__(self, illumination_angle_deg: float = 0.0) -> None:
        """Class constructor.

        Args:
            illumination_angle_deg (float): Angle defining the sun position in the plane.
        """
        super().__init__()
        self.illumination_angle_deg = illumination_angle_deg % 360
        self.sun = self.get_povray_object()

    def get_povray_object(
        self,
    ) -> LightSource:  # First dummy modelization. TODO: Change (IN PROGRESS)
        """Retrieve the povray object."""
        ref = datetime.datetime(
            2025, 3, 10, 9, 1, 0
        )  # Datetime Vernal equinox of 2025 UTC
        date = datetime.datetime(
            2025, 3, 10, 9, 1, 0
        )  # TODO: Iterate it so that it takes the date of the simulation

        # Get the difference in seconds
        seconds_difference = (
            date - ref
        ).total_seconds()  # [s] Difference between reference date and current date
        angle = (
            2 * m.pi * seconds_difference / 86164
        )  # [rad] Angle between ECI and ECEF reference frames

        return LightSource(
            [
                earth_sun_distance * m.cos(angle),
                earth_sun_distance * m.cos(OBLIQUITY) * m.sin(angle),
                earth_sun_distance * m.sin(OBLIQUITY) * m.sin(angle),
            ],
            "color",
            [1, 1, 1],
        )
