"""Definition of Sun lightsource."""

from vapory import (
    Object,
    Pigment,
    ImageMap,
    Texture,
    Finish,
    Sphere
)
from space_based_telescope_image_generator.objects.astral_object import AstralObject
from space_based_telescope_image_generator.utils.constants import (
    sun_oort_cloud_distance
)

class StarMap(AstralObject):
    """Definition of the Starmap background."""

    def __init__(self)->None:
        """Class constructor."""
        self.starmap = self.get_povray_object()
    
    def get_povray_object(self)->Object:
        """Return the Starmap object.

        Returns:
            Object: _description_
        """
        starmap_pigment = Pigment(
            ImageMap(
                "exr",
                '"/resources/images/starmap_2020_16k_gal.exr"',
                "map_type",
                2,
                "interpolate",
                2,
            )
        )
        starmap_texture = Texture(
            starmap_pigment,
            Finish(
                "diffuse", 0,  # No diffuse reflection
                "ambient", 1,  # Fully self-illuminated
                "emission", 1  # Emits light to appear visible
            )
        )
        return Object(Sphere([0, 0, 0], sun_oort_cloud_distance), starmap_texture, "hollow") #Centered on Earth TODO: Change that ?