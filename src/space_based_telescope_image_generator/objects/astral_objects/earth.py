"""Define a basic Earth."""

from vapory import (
    BumpMap,
    Normal,
    Object,
    Sphere,
    Texture,
    Pigment,
    Finish,
    ImageMap,
    Union,
    Media,
    Scattering,
    Density,
    Interior,
)
from space_based_telescope_image_generator.objects.astral_objects.astral_object import AstralObject
from space_based_telescope_image_generator.utils.configuration import MainConfig
from space_based_telescope_image_generator.utils.constants import (
    earth_radius,
    atmosphere_radius,
)


class Earth(AstralObject):
    def __init__(self) -> None:
        """Constructor for BasicEarth."""

        # Combine Earth and Clouds into a single model
        self.earth_model = self.get_povray_object()

    def _add_scattering(self) -> Object:
        """Create a Rayleigh scattering atmosphere using Scattering with a density function.

        Based on https://news.povray.org/povray.binaries.tutorials/message/<op.uth9wqlmm1sclq%40pignouf>/#<op.uth9wqlmm1sclq%40pignouf>

        Returns:
            Object: A hollow sphere with Rayleigh scattering and variable density.
        """

        # Rayleigh parameters
        base_rayleigh_power = 6.7
        rayleigh_factor = 1.15e-2  # Montecarlo
        rayleigh_power = base_rayleigh_power * rayleigh_factor

        lambda_red = 650.0  # nm
        lambda_green = 555.0  # nm
        lambda_blue = 460.0  # nm
        rayleigh_scattering_color = [
            (lambda_blue / lambda_red) ** 4,
            (lambda_blue / lambda_green) ** 4,
            1.0,
        ]

        # Reyleigh Media with variable density
        rayleigh_media = Media(
            Scattering(
                1, rayleigh_scattering_color, "extinction", 1.0  # Type Rayleigh
            ),
            Density(
                "function",
                "{ 1.0 * exp(-%f * (sqrt(x*x + (y + %f)*(y + %f) + z*z) - %f) / %f) }"
                % (
                    rayleigh_power,
                    earth_radius,
                    earth_radius,
                    earth_radius,
                    atmosphere_radius - earth_radius,
                ),
            ),
        )

        atmosphere_texture = Texture(
            Pigment("rgbt", [0, 0, 0, 1]),  # Transparent atmosphere
            Finish("ambient", 0, "diffuse", 0),
        )

        # Atmospheric sphere with Rayleigh Media
        return Object(
            Sphere([0, 0, 0], atmosphere_radius),
            atmosphere_texture,
            "hollow",
            Interior(rayleigh_media),
        )

    def _create_earth(self) -> Object:
        """Create and return the Earth object.

        Returns:
            (Object): The textured Earth.

        """
        earth_pigment = Pigment(
            ImageMap(
                "tiff",
                f'"/resources/images/earth_color_{MainConfig().resolution_configuration.earth_texture_resolution}.tif"',
                "map_type",
                1,
                "interpolate",
                2,
            )
        )
        earth_normal = Normal(
            BumpMap(
                f'"/resources/images/topography_{MainConfig().resolution_configuration.earth_topography_resolution}.png"',
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
        return Object(
            Sphere([0, 0, 0], earth_radius), earth_texture, "rotate", [0, 25, 0]
        )

    def _create_clouds(self) -> Object:
        """Create and return the Clouds object.

        Returns:
            (Object): Textured clouds.

        """
        clouds_pigment = Pigment(
            ImageMap(
                "tiff",
                f'"/resources/images/earth_clouds_{MainConfig().resolution_configuration.earth_clouds_resolution}.tif"',
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
        scattering = self._add_scattering()

        if MainConfig().resolution_configuration.modelize_scattering:
            return Union(clouds, earth, scattering)
        return Union(clouds, earth)
