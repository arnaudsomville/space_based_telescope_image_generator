"""Exemple on how to use the Scene Manager."""

from pathlib import Path
from space_based_telescope_image_generator.objects.targets.rusty_satellite import (
    RustySatellite,
)
from space_based_telescope_image_generator.objects.tracking_satellite import (
    TrackingSatellite,
)
from space_based_telescope_image_generator.objects.targets.primitive_cubesat import (
    PrimitiveCubesat,
)

from space_based_telescope_image_generator.processings.attitude import ConstantSlewAttitudeModel
from space_based_telescope_image_generator.processings.propagation import KeplerianModel
from space_based_telescope_image_generator.processings.scene_manager import SceneManager
from space_based_telescope_image_generator.utils.constants import earth_radius

sat_altitude = 5000
relative_distance_to_satellite = 0.05

TLE_sat = [
    "1 55044U 23001AM  25005.04515951  .02585999  11606-1  26070-2 0  9995",
    "2 55044  97.3788  79.4722 0006145 286.1743  73.8866 16.13983607112084",
]

# Firstly we define a target
cubesat = PrimitiveCubesat(
    kepler_dynamic_model=KeplerianModel.from_tle(TLE_sat),
    attitude_model=ConstantSlewAttitudeModel([0,0,0], 10), #Constant Slew of 10deg/s on each axis
    size=10,
    thickness=1,
)
## Second target type, you can either choose the cubesat or this one
rusty_sat = RustySatellite(
    kepler_dynamic_model=KeplerianModel.from_tle(TLE_sat),
    attitude_model=ConstantSlewAttitudeModel([0,0,0], 10), #Constant Slew of 10deg/s on each axis
)
rusty_sat.position = [
    earth_radius + sat_altitude - relative_distance_to_satellite,
    relative_distance_to_satellite,
    0,
]  # Easier for the example, orbit are mainly for propagation purpose.

# Then we define a Satellite (our camera)
camera_fov = 60
camera_resolution = (1920, 1080)
TLE_track = [
    "1 55044U 23001AM  25005.04515951  .02585999  11606-1  26070-2 0  9995",
    "2 55044  97.3788  79.4722 0006145 286.1743  73.8866 16.13983607112084",
]

satellite = TrackingSatellite(
    kepler_dynamic_model=KeplerianModel.from_tle(TLE_track),
    fov=camera_fov,
    image_height=camera_resolution[1],
    image_width=camera_resolution[0],
)
satellite.position = [earth_radius + sat_altitude, 0, 0]  # E
satellite.target_pointing(
    cubesat.get_position()
)  # We explicitely say that the satellite has to point to the target

# Finally we create a scene with those 2 objects and generate an image.
scene_manager = SceneManager(target=cubesat, satellite=satellite, sun_direction_deg=0)

scene_manager.render_image(ouput_image_path=Path.home().joinpath("exemple_image.png"))
