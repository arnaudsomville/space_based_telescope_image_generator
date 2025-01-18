"""Define the rusty satellite."""

from space_based_telescope_image_generator.objects.targets.target_object import (
    TargetObject,
)
from vapory import Object

from space_based_telescope_image_generator.utils.configuration import MainConfig


class RustySatellite(TargetObject):
    """Define the Rusty Satellite."""

    def __init__(
        self,
        position: list[float],
        attitude: list[float],
    ) -> None:
        """
        Constructeur de la classe RustySatellite.

        :param position: Position absolue du Satellite [x, y, z].
        :param attitude: Rotation du Satellite sur les axes [x, y, z] (en degrés).
        """
        geom_file = f"/{MainConfig().path_management.models_path}/{MainConfig().online_resources.rusty_satellite_resources.model_name}/{MainConfig().online_resources.rusty_satellite_resources.geom_inc_file}"
        super().__init__(position, attitude, [str(geom_file)])
        self.rusty_satellite = self.get_povray_object()

    def get_povray_object(self) -> Object:
        """Return povray object.

        Returns:
            Object: Povray object.
        """
        rusty_sat = Object(
            MainConfig().online_resources.rusty_satellite_resources.povray_id
        )
        return rusty_sat.add_args(
            [
                "scale",
                0.001,  # Project scale in km, satelite uses meters
                "rotate",
                self.attitude,
                "translate",
                self.position,
            ]
        )
