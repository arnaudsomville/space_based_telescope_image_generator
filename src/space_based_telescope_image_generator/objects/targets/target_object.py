"""Target object."""

from vapory import POVRayElement

from abc import ABC, abstractmethod

from space_based_telescope_image_generator.processings.propagation import KeplerianModel


class TargetObject(ABC, POVRayElement):
    """Base for targets."""

    def __init__(
        self,
        kepler_dynamic_model: KeplerianModel,
        attitude: list[float],
        additional_includes: list[str] = [],
    ) -> None:
        """_summary_

        Args:
            position (list[float]): Position vector in km.
            rotation (list[float]): Rotation vector of the object in degree.
            additional_includes: list[str]: Important includes.

        """
        super().__init__()
        self.kepler_dynamic_model = kepler_dynamic_model
        self.position = kepler_dynamic_model.keplerian2cartesian()[0]
        self.attitude = attitude
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

    def propagate_position(self, propagation_time: float, dt_s: float) -> dict[float, tuple[float, float, float]]:
        """Propagate the orbite for an amount of time.

        Args:
            propagation_time (float): Amount of seconds to propagate.
            dt_s (float): Delta t between two steps.

        Returns:
            dict[float, tuple[float, float, float]]: Returns a dictionnary associating a timestamp with
            the positions [km] in EME2000.
        """
        return self.kepler_dynamic_model.propagate(propagation_time, dt_s)[0]

    def propagate_attitude(self, propagation_time: float, dt_s: float) -> dict[float, float]:
        """Propagate the orbite for an amount of time.

        Args:
            propagation_time (float): Amount of seconds to propagate.
            dt_s (float): Delta t between two steps.

        Returns:
            dict[float, tuple[float, float, float]]: Returns a dictionnary associating a timestamp with
            the attitudes [deg] in LVLH.

        """
        raise NotImplementedError("TODO: Implement")


    @abstractmethod
    def get_povray_object(self):
        """Retrieve the povray object."""
        pass
