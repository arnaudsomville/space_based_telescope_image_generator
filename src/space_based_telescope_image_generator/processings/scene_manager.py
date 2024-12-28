"""Manage the scene definition and image generation."""

from pathlib import Path
from space_based_telescope_image_generator.objects.astral_objects.earth import Earth
from space_based_telescope_image_generator.objects.astral_objects.starmap import StarMap
from space_based_telescope_image_generator.objects.astral_objects.sun import Sun
from space_based_telescope_image_generator.objects.targets.target_object import TargetObject
from space_based_telescope_image_generator.objects.tracking_satellite import TrackingSatellite
from space_based_telescope_image_generator.utils.configuration import MainConfig
from space_based_telescope_image_generator.utils.home_folder_management import verify_home_folder
from vapory import Scene

from space_based_telescope_image_generator.utils.resolution_checker import check_resolutions


class SceneManager:
    """Class managing the creation of a scene with all the mandatory elements (satellite, target, Earth, Background)."""

    def __init__(self, target: TargetObject, satellite: TrackingSatellite,sun_direction_deg: float = 0.0):
        """Class constructor."""
        verify_home_folder()
        check_resolutions()
        self.earth = Earth().get_povray_object()
        self.background = StarMap().get_povray_object()
        self.sun = Sun(sun_direction_deg).get_povray_object()
        self.verify_satellite(satellite)
        self.satellite = satellite
        self.verify_target(target)
        self.target = target

    def verify_target(self, target: TargetObject)->None:
        """Set the target.

        Args:
            target (TargetObject): Target of the satellite.

        """
        if not isinstance(target, TargetObject):
            raise ValueError("Provided object is not a valid Target.")
        self.target = target
    
    def verify_satellite(self, satellite: TrackingSatellite)->None:
        """Set the target.

        Args:
            target (TargetObject): Target of the satellite.

        """
        if not isinstance(satellite, TrackingSatellite):
            raise ValueError("Provided object is not a valid TrackingSatellite.")
        self.target = satellite
    
    def render_image(self, ouput_image_path: Path)->None:
        """Render the image.

        Args:
            ouput_image_path (Path): Path where the image will be saved (should be a file).
        """
        if ouput_image_path.is_dir():
            raise ValueError('Provided path is a folder.')
        home_folder = Path.home().joinpath(MainConfig().path_management.home_folder)
        resources_folder = home_folder.joinpath(MainConfig().path_management.resources_path)

        ouput_image_path.parent.mkdir(parents=True, exist_ok=True)

        scene = Scene(
            self.satellite.get_camera(),
            objects=[
                self.background,
                self.sun,
                self.earth,
                self.target.get_povray_object()
            ],
            included=["metals.inc", "textures.inc"],
        )

        # Rendu
        output_file = str(ouput_image_path)
        scene.render(
            output_file,
            width=self.satellite.image_width,
            height=self.satellite.image_height,
            tempfile="temp.pov",
            docker=True,
            resources_folder=str(resources_folder),
        )

    def render_video(self, framerate: int, duration_s: int, output_folder: Path)->Path:
        """Render a video.

        Args:
            framerate (int): Video Framerate.
            duration_s (int): _description_
            output_folder (Path): _description_

        Returns:
            Path: _description_
        """
        #Should be an image generation loop which, at each step will :
        #- Update target and satellite position using their set_position method TODO: Implement Orbital Mechanic + Propagation
        #- Update their attitude using self.target.set_attitude and self.satellite.set_target(self.target) TODO: Implement a methode for rotation propagation ?
        #- Generate a new image in the output folder with an incremented name
        #At the end all the generated images should be concatenated in a video / gif
        raise NotImplementedError("TODO: Implement")