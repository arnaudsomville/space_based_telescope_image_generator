"""Definition of Sun lightsource."""

from vapory import (
    LightSource
)
from space_based_telescope_image_generator.objects.astral_objects.astral_object import AstralObject
from space_based_telescope_image_generator.utils.constants import (
    earth_sun_distance
)
import numpy as np

class Sun(AstralObject):
    """Definition of sun being the lightsource.

    Args:
        AstralObject (_type_): _description_
    """

    def __init__(self, illumination_angle_deg: float = 0.0)->None:
        """Class constructor.
        
        Args:
            illumination_angle_deg (float): Angle defining the sun position in the plane.
        """
        self.illumination_angle_deg = illumination_angle_deg % 360
        self.sun = self.get_povray_object()

    def get_povray_object(self)->LightSource:  #First dummy modelization. TODO: Change
        """Retrieve the povray object."""
        return LightSource(
            [earth_sun_distance*np.cos(np.deg2rad(self.illumination_angle_deg)), earth_sun_distance*np.sin(np.deg2rad(self.illumination_angle_deg)),0],
            "color",
            [1, 1, 1],
        )
