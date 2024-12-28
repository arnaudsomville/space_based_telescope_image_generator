"""Verify that the resolutions provided in conf exist."""

from space_based_telescope_image_generator.utils.configuration import MainConfig


earth_texture_resolutions = ["10K", "21K", "43K"]
earth_topography_resolutions = ["5k", "10k", "21K"]
earth_clouds_resolutions = ["8K", "43K"]
starmap_resolutions = ["4k", "8k", "16k", "32k"]


def check_resolutions() -> None:
    """Raise an assertion error if a resolution provided in the configuration file is incorrect."""
    assert (
        MainConfig().resolution_configuration.earth_texture_resolution
        in earth_texture_resolutions
    ), f"Invalid resolution configuration, please modify the configuration file with one of the available resolutions.\nCorrect resolutions available for earth_texture_resolution : {earth_texture_resolutions}"
    assert (
        MainConfig().resolution_configuration.earth_topography_resolution
        in earth_topography_resolutions
    ), f"Invalid resolution configuration, please modify the configuration file with one of the available resolutions.\nCorrect resolutions available for earth_topography_resolution : {earth_topography_resolutions}"
    assert (
        MainConfig().resolution_configuration.earth_clouds_resolution
        in earth_clouds_resolutions
    ), f"Invalid resolution configuration, please modify the configuration file with one of the available resolutions.\nCorrect resolutions available for earth_clouds_resolution : {earth_clouds_resolutions}"
    assert (
        MainConfig().resolution_configuration.starmap_resolution in starmap_resolutions
    ), f"Invalid resolution configuration, please modify the configuration file with one of the available resolutions.\nCorrect resolutions available for starmap_resolution : {starmap_resolutions}"
