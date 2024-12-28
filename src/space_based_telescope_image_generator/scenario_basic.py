from pathlib import Path
from vapory import LightSource, Scene, Background

from space_based_telescope_image_generator.objects.tracking_satellite import (
    TrackingSatellite,
)
from space_based_telescope_image_generator.objects.basic_earth import BasicEarth
from space_based_telescope_image_generator.objects.primitive_cubesat import (
    PrimitiveCubesat,
)
from space_based_telescope_image_generator.utils.configuration import MainConfig
from space_based_telescope_image_generator.utils.constants import (
    earth_radius,
)

# Définir les constantes
sat_altitude = 1000.0  # Altitude du satellite en km
relative_distance = 0.05  # Distance relative pour positionner le CubeSat
fov_degree = 60  # Champ de vision en degrés
cube_sat_size = 0.0001  # Taille du CubeSat en km (échelle exagérée)
cube_sat_thk = 0.00001  # Épaisseur des faces du CubeSat

# Chemin des images
home_folder = Path.home().joinpath(MainConfig().path_management.home_folder)
resources_folder = home_folder.joinpath(MainConfig().path_management.resources_path)
# Source de lumière simulant le Soleil
sun = LightSource(
    [75000000, 0, 75000000],  # Position approximative du Soleil
    "color",
    [1, 1, 1],
    "parallel",
    "point_at",
    [0, 0, 0],
)

# Fond noir
background = Background("color", [0, 0, 0])


earth = BasicEarth().get_povray_object()

cubesat = PrimitiveCubesat(
    position=[0, relative_distance, earth_radius + sat_altitude - relative_distance],
    rotation=[45, 45, 45],
    size=10,
    thickness=1,
)

# Définition de la caméra
spy_satellite = TrackingSatellite(
    position=[0, 0, earth_radius + sat_altitude], fov=fov_degree
)
spy_satellite.target_pointing(cubesat.get_position())

# Scène
scene = Scene(
    spy_satellite.get_camera(),
    objects=[background, sun, earth, cubesat.get_cubesat()],
    included=["metals.inc", "textures.inc"],
)
print(
    f"Relative distance to the target : {spy_satellite.compute_relative_distance(cubesat)}"
)
# Rendu
output_folder = Path.home()
output_file = str(output_folder.joinpath("earth_and_cubesat_render.png"))
scene.render(
    output_file,
    width=1920,
    height=1080,
    tempfile="temp.pov",
    docker=True,
    resources_folder=str(resources_folder),
)

print("Rendu terminé :", output_file)
