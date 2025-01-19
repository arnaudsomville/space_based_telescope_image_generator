"""File with the definition of attitude computation."""

from abc import ABC, abstractmethod
import numpy as np
from numpy.typing import NDArray


class AttitudeDynamicModel(ABC):
    """Define how a target attitude will evolve."""
    def __init__(
            self,
            init_pos: tuple[float, float, float],
        )->None:
        """Class Constructor."""
        self.init_pos = init_pos

    def propagate(
            self,
            propagation_time: float,
            dt_s: float
        )->list[tuple[float,float,float]]:
        """_summary_

        Args:
            propagation_time (float): Amount of seconds to propagate.
            dt_s (float): Delta t between two steps.

        Returns:
            list[tuple[float,float,float]]: _description_
        """
        vel_profile = self.angular_velocity_profile_maker(propagation_time, dt_s)

        attitudes: list[tuple[float,float,float]] = []
        last_pos = self.init_pos
        for vel in vel_profile:
            attitude_n = last_pos + np.array(vel)*dt_s
            attitudes.append(
                (
                    attitude_n[0] % 360,
                    attitude_n[1] % 360,
                    attitude_n[2] % 360,
                )
            )
            last_pos = np.array(attitudes[len(attitudes)-1])
        return attitudes


    @abstractmethod
    def angular_velocity_profile_maker(
            self,
            propagation_time: float,
            dt_s: float
        )->list[tuple[float,float,float]]:
        """Abstract method used to define an angular velocity profile that will be used for the computation.

        The objective of this abstract method is to be able to define easily an angular velocity profile depending
        on the scenario. You might want to modelize constant slew or slew correction profile, etc... just implement
        this method in a child class. You shouldn't have to modify the propagate method.

        Args:
            propagation_time (float): Amount of seconds to propagate.
            dt_s (float): Delta t between two steps.

        Returns:
            list[tuple[float,float,float]]: list of np.array containing angular velocities for each axis.

        """

class ConstantSlewAttitudeModel(AttitudeDynamicModel):
    """Attitude Dynamic in case of constant slew on all axis."""
    def __init__(
            self,
            init_pos: tuple[float, float, float],
            slew_deg_s: float
        )->None:
        """Class Constructor."""
        super().__init__(init_pos)
        self.slew_deg_s = slew_deg_s
    
    def angular_velocity_profile_maker(
            self,
            propagation_time: float,
            dt_s: float
        )->list[tuple[float,float,float]]:
        """In this case, we define a list of angular speed vector with the same constant value in all axis. 

        Args:
            propagation_time (float): Amount of seconds to propagate.
            dt_s (float): Delta t between two steps.

        Returns:
            list[tuple[float,float,float]]: list of np.array containing angular velocities for each axis.

        """
        vel_profile: list[tuple[float,float,float]] = []
        for _ in range(int(propagation_time / dt_s)):
            vel_profile.append(
                [
                    self.slew_deg_s,
                    self.slew_deg_s,
                    self.slew_deg_s,
                ]
            )
        return vel_profile