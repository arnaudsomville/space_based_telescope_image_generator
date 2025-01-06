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

from space_based_telescope_image_generator.processings.scene_manager import SceneManager
from space_based_telescope_image_generator.utils.constants import earth_radius

sat_altitude = 5000
relative_distance_to_satellite = 0.05

# Firstly we define a target
cubesat = PrimitiveCubesat(
    position=[
        earth_radius + sat_altitude - relative_distance_to_satellite,
        relative_distance_to_satellite,
        0,
    ],  # TODO: Define position from Orbit
    attitude=[45, 45, 45],  # Permits to rotate the satellite
    size=10,
    thickness=1,
)
## Second target type, you can either choose the cubesat or this one
rusty_sat = RustySatellite(
    position=[
        earth_radius + sat_altitude - relative_distance_to_satellite,
        relative_distance_to_satellite,
        0,
    ],  # TODO: Define position from Orbit
    attitude=[45, 45, 45],  # Permits to rotate the satellite
)


# Then we define a Satellite (our camera)
camera_fov = 60
camera_resolution = (1920, 1080)

satellite = TrackingSatellite(
    position=[earth_radius + sat_altitude, 0, 0],  # TODO: Define position from Orbit
    fov=camera_fov,
    image_height=camera_resolution[1],
    image_width=camera_resolution[0],
)
satellite.target_pointing(
    cubesat.get_position()
)  # We explicitely say that the satellite has to point to the target

# Finally we create a scene with those 2 objects and generate an image.
scene_manager = SceneManager(target=rusty_sat, satellite=satellite, sun_direction_deg=0)

scene_manager.render_image(ouput_image_path=Path.home().joinpath("exemple_image.png"))
