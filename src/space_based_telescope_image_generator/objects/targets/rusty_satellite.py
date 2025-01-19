"""Define the rusty satellite."""

from space_based_telescope_image_generator.objects.targets.target_object import (
    TargetObject,
)
from vapory import Object

from space_based_telescope_image_generator.processings.attitude import AttitudeDynamicModel
from space_based_telescope_image_generator.processings.propagation import KeplerianModel
from space_based_telescope_image_generator.utils.configuration import MainConfig


class RustySatellite(TargetObject):
    """Define the Rusty Satellite."""

    def __init__(
        self,
        kepler_dynamic_model: KeplerianModel,
        attitude_model: AttitudeDynamicModel,
    ) -> None:
        """
        Constructeur de la classe RustySatellite.

            kepler_dynamic_model (KeplerianModel): Orbital Dynamic of the satellite.
            attitude_model (AttitudeDynamicModel): Attitude dynamic of the satellite.
        """
        geom_file = f"/{MainConfig().path_management.models_path}/{MainConfig().online_resources.rusty_satellite_resources.model_name}/{MainConfig().online_resources.rusty_satellite_resources.geom_inc_file}"
        super().__init__(kepler_dynamic_model, attitude_model, [str(geom_file)])
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
