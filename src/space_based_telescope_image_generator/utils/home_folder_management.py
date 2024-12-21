"""Verify the integrity of home folder."""

from pathlib import Path
import shutil
from space_based_telescope_image_generator.utils.configuration import MainConfig
from gdown import download_folder


def verify_home_folder() -> None: # pragma: no cover
    """Create the home folder if needed with all the needed resources."""
    home_folder = Path.home().joinpath(MainConfig().path_management.home_folder)
    home_folder.mkdir(parents=True, exist_ok=True)

    #Copy conf in home
    conf_file = home_folder.joinpath("configuration.yaml")
    if not conf_file.exists():
        shutil.copy(
            Path(__file__).parents[1].joinpath("configuration_template.yaml"), conf_file
        )
    
    image_path = home_folder.joinpath(MainConfig().path_management.images_path)
    
    #Download NASA Assets
    download_gdrive_folder(
        MainConfig().online_resources.nasa_earth_resources.nasa_resources_link,
        image_path,
        MainConfig().online_resources.nasa_earth_resources.files
    )

def download_gdrive_folder( # pragma: no cover
    gdrive_link: str, output_folder: Path, required_files: list[str]
) -> None:
    """Download a shared folder from Google Drive and ensure required files are present.

    This method verifies the existence of required files in the output folder
    before and after downloading. Only missing files are downloaded.

    Args:
        gdrive_link (str): Google Drive folder link.
        output_folder (Path): Local folder where files will be downloaded.
        required_files (list[str]): List of expected files to verify completeness.

    Raises:
        ValueError: If the Google Drive link or output folder is invalid.
        RuntimeError: If required files are still missing after download.
    """
    if not gdrive_link:
        raise ValueError("The Google Drive link cannot be empty.")
    if not isinstance(output_folder, Path):
        raise ValueError("The output folder must be an instance of pathlib.Path.")

    # Create the output folder if it doesn't exist
    output_folder.mkdir(parents=True, exist_ok=True)

    # Check for missing files
    missing_files = [
        file_name for file_name in required_files
        if not output_folder.joinpath(file_name).exists()
    ]

    if not missing_files:
        print("All required files are already downloaded.")
        return

    print(f"Missing files detected: {missing_files}")
    print("Downloading missing files...")

    # Download missing files
    download_folder(gdrive_link, output=str(output_folder))

    # Re-check for missing files
    remaining_files = [
        file_name for file_name in missing_files
        if not output_folder.joinpath(file_name).exists()
    ]

    if remaining_files:
        raise RuntimeError(f"Failed to download the following files: {remaining_files}")

    print("All required files have been successfully downloaded.")

if __name__ == "__main__":  # pragma: no cover
    verify_home_folder()