"""Manage the scene definition and image generation."""

from pathlib import Path
from PIL import Image
from typing import Union
from space_based_telescope_image_generator.objects.astral_objects.astral_object import (
    AstralObject,
)
from space_based_telescope_image_generator.objects.astral_objects.earth import Earth
from space_based_telescope_image_generator.objects.astral_objects.starmap import StarMap
from space_based_telescope_image_generator.objects.astral_objects.sun import Sun
from space_based_telescope_image_generator.objects.targets.target_object import (
    TargetObject,
)
from space_based_telescope_image_generator.objects.tracking_satellite import (
    TrackingSatellite,
)
from space_based_telescope_image_generator.utils.configuration import MainConfig
from space_based_telescope_image_generator.utils.home_folder_management import (
    verify_home_folder,
)
from vapory import Scene

from space_based_telescope_image_generator.utils.resolution_checker import (
    check_resolutions,
)


class SceneManager:
    """Class managing the creation of a scene with all the mandatory elements (satellite, target, Earth, Background)."""

    def __init__(
        self,
        target: TargetObject,
        satellite: TrackingSatellite,
        sun_direction_deg: float = 0.0,
    ):
        """Class constructor."""
        verify_home_folder()
        check_resolutions()
        self.earth = Earth()
        self.background = StarMap()
        self.sun = Sun(sun_direction_deg)
        self.verify_satellite(satellite)
        self.satellite = satellite
        self.verify_target(target)
        self.target = target

        self.object_list: list[Union[AstralObject, TargetObject]] = [
            self.background,
            self.sun,
            self.earth,
            self.satellite,
            self.target,
        ]

    def verify_target(self, target: TargetObject) -> None:
        """Set the target.

        Args:
            target (TargetObject): Target of the satellite.

        """
        if not isinstance(target, TargetObject):
            raise ValueError("Provided object is not a valid Target.")
        self.target = target

    def verify_satellite(self, satellite: TrackingSatellite) -> None:
        """Set the target.

        Args:
            target (TargetObject): Target of the satellite.

        """
        if not isinstance(satellite, TrackingSatellite):
            raise ValueError("Provided object is not a valid TrackingSatellite.")
        self.target = satellite

    def check_includes(self) -> list[str]:
        """Retrieve important includes.

        Returns:
            list[str]: Libraries /files to be included in the POVRy script.

        """
        include_list = []
        for obj in self.object_list:
            include_list.extend(obj.additional_includes)

        return list(set(include_list))

    def render_image(self, ouput_image_path: Path) -> None:
        """Render the image.

        Args:
            ouput_image_path (Path): Path where the image will be saved (should be a file).
        """
        if ouput_image_path.is_dir():
            raise ValueError("Provided path is a folder.")
        home_folder = Path.home().joinpath(MainConfig().path_management.home_folder)
        resources_folder = home_folder.joinpath(
            MainConfig().path_management.resources_path
        )
        ouput_image_path.parent.mkdir(parents=True, exist_ok=True)

        scene = Scene(
            self.satellite.get_camera(),
            objects=[
                self.sun.get_povray_object(),
                self.earth.get_povray_object(),
                self.target.get_povray_object(),
                self.background.get_povray_object(),
            ],
            included=self.check_includes(),
            global_settings=[
                "max_trace_level",
                128,
                "adc_bailout",
                1e-15,
                "assumed_gamma",
                1.0,
            ],
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

    def render_video(
        self, framerate: int, duration_s: int, output_folder: Path
    ) -> Path:
        """Render a video.

        Args:
            framerate (int): Image per seconds (can be < 0).
            duration_s (int): Total video duration.
            output_folder (Path): Path to the output folder.

        Returns:
            Path: _description_
        """
        delta_t = 1/framerate
        step_images_folder = output_folder.joinpath("steps")
        step_images_folder.mkdir(parents=True, exist_ok=True)

        # Orbital Propagations
        target_positions = self.target.propagate_position(duration_s, delta_t)
        sat_positions = self.satellite.propagate_position(duration_s, delta_t)

        #Attitude propagation
        target_attitudes = self.target.propagate_attitude(duration_s, delta_t)

        #TODO: Add astral propagation

        image_list: list[Path] = []

        for step_i, (sat_pos, target_pos, target_att) in enumerate(zip(sat_positions, target_positions, target_attitudes)):
            print(f"Generating image {step_i + 1} out of {len(target_positions)}")
            # Set satellite position & attitude
            self.satellite.position = sat_pos
            self.satellite.target_pointing(target_pos)
            
            # Set target position & attitude
            self.target.position = target_pos
            self.target.attitude = target_att

            #Render image
            image_path = step_images_folder.joinpath(f"image_{step_i + 1}.png")
            image_list.append(image_path)
            self.render_image(
                ouput_image_path=image_path
            )
        

        # Open images and store them as a list of PIL Image objects
        frames = [Image.open(image) for image in image_list]

        # Save as a GIF
        gif_path = output_folder.joinpath("rendered_video.gif")
        frames[0].save(
            gif_path,
            save_all=True,
            append_images=frames[1:],
            duration=int(delta_t*1000),
            loop=0
        )
        return gif_path