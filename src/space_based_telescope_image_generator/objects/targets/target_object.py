"""Target object."""

from vapory import POVRayElement

from abc import ABC, abstractmethod

from space_based_telescope_image_generator.processings.attitude import AttitudeDynamicModel
from space_based_telescope_image_generator.processings.propagation import KeplerianModel


class TargetObject(ABC, POVRayElement):
    """Base for targets."""

    def __init__(
        self,
        kepler_dynamic_model: KeplerianModel,
        attitude_model: AttitudeDynamicModel,
        additional_includes: list[str] = [],
    ) -> None:
        """_summary_

        Args:
            kepler_dynamic_model (KeplerianModel): Orbital Dynamic of the satellite.
            attitude_model (AttitudeDynamicModel): Attitude dynamic of the satellite.
            additional_includes: list[str]: Important includes.

        """
        super().__init__()
        self.kepler_dynamic_model = kepler_dynamic_model
        self.position = kepler_dynamic_model.keplerian2cartesian()[0]
        self.attitude_model = attitude_model
        self.attitude = attitude_model.init_pos
        self.additional_includes = additional_includes

    def get_position(self) -> list[float]:
        """Retrieve object's position.

        Returns:
            list[float]: Position.
        """
        return self.position

    def get_attitude(self) -> list[float]:
        """Retrieve object's attitude.

        Returns:
            list[float]: attitude.
        """
        return self.attitude

    def propagate_position(
        self, propagation_time: float, dt_s: float
    ) -> list[tuple[float, float, float]]:
        """Propagate the orbite for an amount of time.

        Args:
            propagation_time (float): Amount of seconds to propagate.
            dt_s (float): Delta t between two steps.

        Returns:
            list[tuple[float, float, float]]: Returns a list of positions [km] in EME2000.
        """
        return self.kepler_dynamic_model.propagate(propagation_time, dt_s)[0]

    def propagate_attitude(
        self, propagation_time: float, dt_s: float
    ) -> list[tuple[float, float, float]]:
        """Propagate the orbite for an amount of time.

        Args:
            propagation_time (float): Amount of seconds to propagate.
            dt_s (float): Delta t between two steps.

        Returns:
            list[tuple[float, float, float]]: Returns a list of attitudes [deg] in LVLH.

        """
        return self.attitude_model.propagate(propagation_time,dt_s)

    @abstractmethod
    def get_povray_object(self):
        """Retrieve the povray object."""
        pass
