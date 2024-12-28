"""Definition of Sun lightsource."""

from vapory import Object, Pigment, ImageMap, Texture, Finish, Sphere
from space_based_telescope_image_generator.objects.astral_objects.astral_object import (
    AstralObject,
)
from space_based_telescope_image_generator.utils.configuration import MainConfig
from space_based_telescope_image_generator.utils.constants import starmap_sphere_radius


class StarMap(AstralObject):
    """Definition of the Starmap background."""

    def __init__(self) -> None:
        """Class constructor."""
        self.starmap = self.get_povray_object()

    def get_povray_object(self) -> Object:
        """Return the Starmap object.

        Returns:
            Object: _description_
        """
        starmap_pigment = Pigment(
            ImageMap(
                "exr",
                f'"/resources/images/starmap_2020_{MainConfig().resolution_configuration.starmap_resolution}_gal.exr"',
                "map_type",
                1,
                "interpolate",
                2,
            )
        )

        starmap_texture = Texture(
            starmap_pigment,
            Finish(
                "diffuse",
                0,  # No diffuse reflection
                "ambient",
                1,  # Fully self-illuminated
            ),
        )
        return Object(
            Sphere([0, 0, 0], starmap_sphere_radius),
            starmap_texture,
            "hollow",
            "scale",
            -1,
        )  # Centered on Earth TODO: Change that ?
