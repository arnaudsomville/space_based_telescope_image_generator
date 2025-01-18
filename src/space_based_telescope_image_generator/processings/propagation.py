import math as m
import numpy as np
import re
from datetime import datetime
from numpy.typing import NDArray
import matplotlib.pyplot as plt
from pydantic import BaseModel

from space_based_telescope_image_generator.utils.constants import (
    DAY_SECONDS,
    J2,
    MU,
    PI,
    RE,
)


class KeplerianModel(BaseModel):
    """Class containing Orbital Parameters data."""

    a: float  # Semi-major axis (m)
    e: float  # Eccentricity (-)
    i: float  # Inclination (rad)
    Omega: float  # Longitude of the Right Ascension of the Ascending Node (rad)
    omega: float  # Argument of perigee (rad)
    nu: float  # True anomaly (rad)
    epoch: float  # timestamp (s)

    @classmethod
    def from_tle(cls, TLE: tuple[str, str] | list[str]) -> "KeplerianModel":
        """
        This function extracts the Keplerian elements and date of a space object from a TLE
        and returns an instance of OrbitalParameters.

        Args:
            TLE: tuple[str, str], Two-line element set.

        Returns:
            OrbitalParameters: Instance populated with the extracted Keplerian elements.
        """
        # Cleans the TLE from all multiple spaces, replaces them with single spaces
        for j in range(len(TLE)):  # Runs through all line of the TLE
            count = 0  # While loop safety
            while "  " in TLE[j] and count < 100:
                TLE[j] = re.sub(  # type: ignore
                    r"\s+", " ", TLE[j]
                ).strip()  # Detects and replaces multiple spaces
                count += 1  # Avoids infinite while loop in case of problem
        TLE1 = TLE[0].split(" ")
        TLE2 = TLE[1].split(" ")

        e = float("0." + TLE2[4])  # [-] Eccentricity
        i = float(TLE2[2])  # [deg] Inclination
        Omega = float(TLE2[3])  # [deg] Longitude of RAAN
        omega = float(TLE2[5])  # [deg] Argument of perigee
        nu = float(TLE2[6])  # [deg] True anomaly
        MM = float(TLE2[7])  # [rev/day] Mean motion
        T = 86400 / MM  # [s] Orbital period
        a = (MU * (T / (2 * PI)) ** 2) ** (1 / 3)  # [m] Semi-major axis

        year = 2000 + int(float(TLE1[3]) / 1000)  # Associated date
        doy = float(TLE1[3]) % 1000  # Day of the year

        month, day = cls._getDate(year, doy)
        hour, minute, second = cls._s2hms(doy)

        date = datetime(year, month, day, hour, minute, second)

        # Create and return an instance of OrbitalParameters
        return cls(
            a=a, e=e, i=i, Omega=Omega, omega=omega, nu=nu, epoch=date.timestamp()
        )

    @classmethod
    def from_pvt(
        cls,
        position: tuple[float, float, float],
        velocity: tuple[float, float, float],
        epoch: datetime,
    ) -> "KeplerianModel":
        """
        Convert position, velocity, and time (PVT) into Keplerian elements.

        Args:
            position (tuple[float, float, float]): Position in km (x, y, z).
            velocity (tuple[float, float, float]): Velocity in km/s (vx, vy, vz).
            epoch (datetime): Epoch time in UTC.

        Returns:
            OrbitalParameters: Instance with the calculated Keplerian elements.
        """
        # Convert tuples to numpy arrays for easier computation
        pos = np.array(position)
        vel = np.array(velocity)

        # Magnitudes of position and velocity
        r = np.linalg.norm(pos)  # [km]
        v = np.linalg.norm(vel)  # [km/s]

        # Specific angular momentum vector
        h = np.cross(pos, vel)  # [km^2/s]
        h_mag = np.linalg.norm(h)

        # Inclination
        i = np.arccos(h[2] / h_mag)  # [rad]

        # Node line vector
        n = np.cross([0, 0, 1], h)  # [km^2/s]
        n_mag = np.linalg.norm(n)

        # Right ascension of ascending node (RAAN)
        Omega = 0.0 if n_mag == 0 else np.arccos(n[0] / n_mag)  # [rad]
        if n[1] < 0:
            Omega = 2 * np.pi - Omega

        # Eccentricity vector
        e_vec = (np.cross(vel, h) / MU) - (pos / r)  # [-]
        e = np.linalg.norm(e_vec)

        # Argument of perigee
        omega = (
            0.0 if n_mag == 0 or e == 0 else np.arccos(np.dot(n, e_vec) / (n_mag * e))
        )  # [rad]
        if e_vec[2] < 0:
            omega = 2 * np.pi - omega

        # True anomaly
        nu = np.arccos(np.dot(e_vec, pos) / (e * r))  # [rad]
        if np.dot(pos, vel) < 0:
            nu = 2 * np.pi - nu

        # Semi-major axis
        a = 1 / ((2 / r) - (v**2 / MU))  # [km]

        # Return an instance of OrbitalParameters
        return cls(
            a=a * 1000,  # Convert to meters
            e=e,
            i=i,
            Omega=Omega,
            omega=omega,
            nu=nu,
            epoch=int(epoch.timestamp()),  # Convert datetime to timestamp (seconds)
        )

    @classmethod
    def _getDate(cls, y: float, doy: float) -> tuple[int, int]:
        """
        This function finds the date according to the year and the day of the year (doy)

        Args:
            y: float, year (2000+)
            doy: float, day of the year

        Returns:
            month: int, number of the month from 1 to 12
            day: int, number of the date from 1 to 31
        """
        doy = int(
            doy
        )  # Takes the integer part: the fractional part corresponds to hours, minute, second
        dayPerMonth = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

        if y % 4 == 0:  # Leap year
            dayPerMonth[1] += 1  # Adds one day in February

        countDay = 0  # Counts the number of days passed after each month
        count = 0  # While loop safety
        j = 0  # Iteration
        while countDay < doy and count < 100:
            countDay += dayPerMonth[j]
            j += 1
            count += 1
        month = j
        day = doy - countDay + dayPerMonth[month]
        return month, day

    @classmethod
    def _s2hms(cls, doy: float) -> tuple[int, int, int]:
        """
        This function converts the day of the year into the corresponding hour, minute and second

        Args:
            doy: float, day of the year between 0 and 366

        Returns:
            hour: int, number of hours passed since the beginning of the say in UTC
            minute: int, number of minutes passed
            second: int, number of whole seconds passed
        """
        fractional = (
            doy % 1
        )  # Takes the fractional part of the DOY (corresponding to the advancement in the day)
        secondDoy = fractional * 86400  # Converts the fractional part in seconds

        # Initializing the variables
        hour = 0
        minute = 0
        second = 0

        count = 0  # While loop safety
        while secondDoy > 3600 and count < 100:  # Counts the hours
            hour += 1
            secondDoy -= 3600
            count += 1

        count = 0  # While loop safety
        while secondDoy > 60 and count < 100:  # Counts the minutes
            minute += 1
            secondDoy -= 60
            count += 1
        second = int(secondDoy)  # The remainder is the number of seconds

        return hour, minute, second

    def _get_rotation_matrix(self, a: float, u: int) -> NDArray:
        """
        Rotation matrices method

        Args:
            a: float, rotation angle [rad]
            u: int, rotation axis (0 = x, 1 = y, 2 = z)

        Returns:
            Rot: NDArray, 3x3 matrix
        """
        c = np.cos(a)
        s = np.sin(a)
        if u == 0:  # Rotation about the x-axis
            Rot = np.array([[1, 0, 0], [0, c, -s], [0, s, c]])
        elif u == 1:  # Rotation about the y-axis
            Rot = np.array([[c, 0, s], [0, 1, 0], [-s, 0, c]])
        elif u == 2:  # Rotation about the z-axis
            Rot = np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]])
        else:  # Wrong axis number: error
            Rot = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
            print("Error: wrong axis number provided for rotation matrix")
        return Rot

    def _radius(self) -> float:
        """
        Instantaneous radius of the orbit, given for the current Keplerian elements a, e and nu

        Returns:
            Position radius for a non-circular orbit, float
        """
        return self.a * (1 - self.e**2) / (1 + self.e * m.cos(self.nu))

    def keplerian2cartesian(
        self,
    ) -> tuple[tuple[float, float, float], tuple[float, float, float]]:
        """Exposed method used to retrieve PVT in km - km/s from outside.

        Returns:
            tuple[tuple[float, float, float],tuple[float, float, float]]: Position [km] / Speed [km/s]

        """
        pos, vel = self._keplerian2cartesian()

        return (
            (pos[0] / 1000, pos[1] / 1000, pos[2] / 1000),
            (vel[0] / 1000, vel[1] / 1000, vel[2] / 1000),
        )

    def _keplerian2cartesian(self) -> tuple[NDArray, NDArray]:
        """
        Converts the Keplerian elements into state vectors

        Returns:
            r: ECI position vector 3x1, NDArray [m/s]
            rdot: ECI velocity vector 3x1, NDArray [m/s]
        """
        rc = self._radius()
        E = 2 * m.atan2(m.tan(self.nu / 2), m.sqrt((1 + self.e) / (1 - self.e)))
        o = rc * np.array([m.cos(self.nu), m.sin(self.nu), 0])
        odot = (
            m.sqrt(MU * self.a)
            / rc
            * np.array([-m.sin(E), m.sqrt(1 - self.e**2) * m.cos(E), 0])
        )

        r = np.matmul(
            self._get_rotation_matrix(self.Omega, 2),
            np.matmul(
                self._get_rotation_matrix(self.i, 0),
                np.matmul(self._get_rotation_matrix(self.omega, 2), o),
            ),
        )
        rdot = np.matmul(
            self._get_rotation_matrix(self.Omega, 2),
            np.matmul(
                self._get_rotation_matrix(self.i, 0),
                np.matmul(self._get_rotation_matrix(self.omega, 2), odot),
            ),
        )
        return r, rdot

    def compute_jerk_and_acc(
        self, pos: NDArray, vel: NDArray
    ) -> tuple[NDArray, NDArray]:
        """
        Calculates the instantaneous acceleration and jerk vectors

        Args:
            pos: ECI position vector, NDArray 3x1
            vel: ECI velocity vector, NDArray 3x1

        Returns:
            acc: NDArray, ECI acceleration vector 3x1 (m/s2)
            jerk: NDArray, ECI jerk vector 3x1 first time deritative of acceleration (m/s3)
        """
        pos_norm = np.linalg.norm(pos)  # [m] Norm of the positio vector

        if pos_norm == 0:
            return np.zeros(3), np.zeros(
                3
            )  # Special case : position at the origin of the reference frame

        acc2B = -MU * pos / pos_norm**3  # [m/s2] 2-body acceleration

        accJ2 = [  # [m/s2] J2 acceleration
            MU
            / pos_norm**2
            * (RE / pos_norm) ** 2
            * J2
            * (15 / 2 * (pos[2] / pos_norm) ** 2 - 3 / 2)
            * pos[0]
            / pos_norm,
            MU
            / pos_norm**2
            * (RE / pos_norm) ** 2
            * J2
            * (15 / 2 * (pos[2] / pos_norm) ** 2 - 3 / 2)
            * pos[1]
            / pos_norm,
            MU
            / pos_norm**2
            * (RE / pos_norm) ** 2
            * J2
            * (15 / 2 * (pos[2] / pos_norm) ** 2 - 9 / 2)
            * pos[2]
            / pos_norm,
        ]

        acc = acc2B + accJ2
        jerk = -MU * (
            vel / pos_norm**3 - 3 * pos * np.dot(pos, vel) / pos_norm**5
        )  # [m/s3] 2-body jerk
        return acc, jerk

    def propagate(
        self, propagation_time: float, dt_s: float
    ) -> tuple[
        dict[float, tuple[float, float, float]], dict[float, tuple[float, float, float]]
    ]:
        """Propagate the orbite for an amount of time.

        Args:
            propagation_time (float): Amount of seconds to propagate.
            dt_s (float): Delta t between two steps.

        Returns:
            tuple[dict[float, tuple[float, float, float]], dict[float, tuple[float, float, float]]]: Returns two dictionnaries
              associating a timestamp with the positions [km]/ instantanate speed [km/s] in EME2000.
        """
        # Initialize arrays to store position and velocity
        pos, vel = self._keplerian2cartesian()
        acc, jerk = self.compute_jerk_and_acc(pos, vel)

        position_dict = {}
        velocity_dict = {}
        # Main simulation loop
        date = self.epoch
        for _ in range(int(propagation_time / dt_s)):
            pos_new: NDArray = (
                pos + vel * dt_s + acc * dt_s**2 / 2 + jerk * dt_s**3 / 6
            )  # [m] Forward Euler, order 3 integration
            vel_new: NDArray = (
                vel + acc * dt_s + jerk * dt_s**2 / 2
            )  # [m/s] Forward Euler, order 2 integration
            date = date + dt_s  # [s] timestamp
            acc, jerk = self.compute_jerk_and_acc(
                pos_new, vel_new
            )  # [m/s2, m/s3] New acceleration and jerk vectors
            position_dict.update(
                {date: (pos_new[0] / 1000, pos_new[1] / 1000, pos_new[2] / 1000)}
            )  # [km] Position array
            velocity_dict.update(
                {date: (pos_new[0] / 1000, pos_new[1] / 1000, pos_new[2] / 1000)}
            )  # [km/s] Velocity array
            pos = pos_new  # [m] Resetting position vector
            vel = vel_new  # [m/s] Resetting velocity vector
        return (position_dict, velocity_dict)


if __name__ == "__main__":
    TLE = [
        "1 55044U 23001AM  25005.04515951  .02585999  11606-1  26070-2 0  9995",
        "2 55044  97.3788  79.4722 0006145 286.1743  73.8866 16.13983607112084",
    ]

    kep = KeplerianModel.from_tle(TLE)

    # Simulation parameters
    nb_days = 1  # [day] Number of days of propagation
    time = DAY_SECONDS * nb_days  # [s] Total time
    dt_s = 5  # [s] Time step of the simulation

    pos_dict, vel_dict = kep.propagate(time, dt_s)

    # Convert lists to numpy arrays
    pos_array = np.array(
        [[pos[0] * 1000, pos[1] * 1000, pos[2] * 1000] for pos in pos_dict.values()]
    )
    vel_array = np.array(
        [[vel[0] * 1000, vel[1] * 1000, vel[2] * 1000] for vel in vel_dict.values()]
    )

    # Plotting the orbit in 3D
    fig2 = plt.figure()
    plt.title("Orbit in ECI")

    # Creating a wireframe for the Earth
    phi = np.linspace(0, 2 * m.pi, 36)  # Angular meshing
    theta = np.linspace(0, m.pi, 18)  # Angular meshing
    A, B = np.meshgrid(theta, phi)
    X = RE * np.sin(A) * np.cos(B)  # X coordinates
    Y = RE * np.sin(A) * np.sin(B)  # Y coordinates
    Z = RE * np.cos(A)  # Z coordinates

    # Plotting the Earth and the trajectory
    eci = fig2.add_subplot(111, projection="3d")
    # Sphere
    eci.plot_wireframe(X, Y, Z, color="c", zorder=1, alpha=0.25)  # type: ignore
    # Trajectory
    eci.plot3D(pos_array[:, 0], pos_array[:, 1], pos_array[:, 2], color="m")  # type: ignore

    # Plotting the ECI coordinates in 2D
    plt.figure()
    # X_ECI
    plt.plot(pos_array[:, 0], color="r")  # type: ignore
    # Y_ECI
    plt.plot(pos_array[:, 1], color="g")  # type: ignore
    # Z_ECI
    plt.plot(pos_array[:, 2], color="b")  # type: ignore
    plt.grid()
    plt.legend(["$X_{ECI}$", "$Y_{ECI}$", "$Z_{ECI}$"])
    plt.title("Coordinates in ECI of the satellite versus time")
    plt.xlabel(f"Time, one step = {dt_s} sec")
    plt.ylabel("ECI coordinates in m")
    plt.show()
