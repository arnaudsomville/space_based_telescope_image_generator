"""Define a basic Earth without Scattering."""

from vapory import (
    POVRayElement,
    BumpMap,
    Normal,
    Object,
    Sphere,
    Texture,
    Pigment,
    PigmentMap,
    Finish,
    ImageMap,
    Union,
)
from space_based_telescope_image_generator.utils.constants import earth_radius


class BasicEarth(POVRayElement):
    def __init__(self) -> None:
        """Constructor for BasicEarth."""

        # Combine Earth and Clouds into a single model
        self.earth_model = self.get_povray_object()
    
    def _add_scattering(self) -> Object:
        """Create a basic scattering sphere.

        Returns:
            Object: Transparent blue sphere.
        """
        scattering_texture = Texture(
            Pigment(
                'rgbt', [0.1, 0.1, 0.9, 0.7]  # Light blue (RGB) with 90% transparency
            ),
            Finish(
                'ambient', 0.1,  # Minimal ambient light
                'diffuse', 0.1   # Low diffuse reflection
            )
        )
        return Object(Sphere([0, 0, 0], (earth_radius + 50)), scattering_texture)

    def _create_earth(self) -> Object:
        """Create and return the Earth object.

        Returns:
            (Object): The textured Earth.

        """
        scattering = self._add_scattering()
        earth_pigment = Pigment(
            ImageMap(
                "tiff",
                '"/resources/images/earth_color_43K.tif"',
                "map_type",
                1,
                "interpolate",
                2,
            )
        )
        earth_normal = Normal(
            BumpMap(
                '"/resources/images/topography_21K.png"',
                "map_type",
                1,
                "interpolate",
                2,
                "bump_size",
                0.05,
            )
        )
        earth_texture = Texture(
            earth_pigment,
            Finish("diffuse", 0.8, "ambient", 0, "specular", 0.2, "roughness", 0.05),
            earth_normal,
        )
        return Union(
            Object(Sphere([0, 0, 0], earth_radius), earth_texture, "rotate", [0, 25, 0]),
            scattering
        )

    def _create_clouds(self) -> Object:
        """Create and return the Clouds object.

        Returns:
            (Object): Textured clouds.

        """
        clouds_pigment = Pigment(
            ImageMap(
                "tiff",
                '"/resources/images/earth_clouds_43K.tif"',
                "map_type",
                1,
                "interpolate",
                2,
                "transmit",
                "all",
                0.8,
            )
        )
        clouds_texture = Texture(
            clouds_pigment, Finish("diffuse", 0.7, "ambient", 0.0, "specular", 0.2)
        )
        return Object(Sphere([0, 0, 0], earth_radius + 10), clouds_texture, "hollow")

    def get_povray_object(self) -> Union:
        """Return an Earth Povray Object.

        Returns:
            Union: Union of ground texture + topography + clouds.
        """
        # Create Earth and Clouds components
        earth = self._create_earth()
        clouds = self._create_clouds()

        return Union(clouds, earth)
