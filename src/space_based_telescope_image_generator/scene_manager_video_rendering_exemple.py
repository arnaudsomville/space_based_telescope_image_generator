"""Exemple on how to use the Scene Manager."""

from datetime import datetime
from pathlib import Path
from space_based_telescope_image_generator.objects.targets.rusty_satellite import (
    RustySatellite,
)
from space_based_telescope_image_generator.objects.tracking_satellite import (
    TrackingSatellite,
)

from space_based_telescope_image_generator.processings.attitude import ConstantSlewAttitudeModel
from space_based_telescope_image_generator.processings.propagation import KeplerianModel
from space_based_telescope_image_generator.processings.scene_manager import SceneManager

# Firstly we define a target

rusty_sat = RustySatellite(
    kepler_dynamic_model=KeplerianModel.from_pvt(
        position=[
            7000,
            0,
            0
        ],
        velocity=[
            0,
            8,
            0
        ],
        epoch=datetime.now()
    ),
    attitude_model=ConstantSlewAttitudeModel([0,0,0], 10) #Constant Slew of 10deg/s on each axis
)

# Then we define a Satellite (our camera)
camera_fov = 20
camera_resolution = (1280, 720)

satellite = TrackingSatellite(
    kepler_dynamic_model=KeplerianModel.from_pvt(
        position=[
            7000.1,
            0,
            0
        ],
        velocity=[
            0,
            8,
            0
        ],
        epoch=datetime.now()
    ),
    fov=camera_fov,
    image_height=camera_resolution[1],
    image_width=camera_resolution[0],
)
satellite.target_pointing(
    rusty_sat.get_position()
)  # We explicitely say that the satellite has to point to the target

# Finally we create a scene with those 2 objects and generate an image.
scene_manager = SceneManager(target=rusty_sat, satellite=satellite, sun_direction_deg=0)

scene_manager.render_video(
    framerate=15,
    duration_s=10,
    output_folder=Path.home().joinpath("exemple_video")
)
