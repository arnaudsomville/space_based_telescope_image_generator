from pathlib import Path
from vapory import BumpMap, Normal, Camera, Object, LightSource, Sphere, Texture, Pigment, Finish, Scene, ImageMap, Box, Union,PigmentMap, Background

from space_based_telescope_image_generator.objects.basic_earth import BasicEarth
from space_based_telescope_image_generator.objects.primitive_cubesat import PrimitiveCubesat

# Définir les constantes
earth_radius = 6378.0  # Rayon de la Terre en km
sat_altitude = 10000.0  # Altitude du satellite en km
relative_distance = 0.05  # Distance relative pour positionner le CubeSat
fov_degree = 60  # Champ de vision en degrés
cube_sat_size = 0.0001  # Taille du CubeSat en km (échelle exagérée)
cube_sat_thk = 0.00001  # Épaisseur des faces du CubeSat

# Chemin des images

# Définition de la caméra
camera = Camera(
    'location', [0, 0, earth_radius + sat_altitude],
    'look_at', [0, 0, 0],
    'angle', fov_degree,
    'right', 'x*image_width/image_height'
)

# Fond noir
background = Background(
    'color', [0, 0, 0]
)

# Source de lumière simulant le Soleil
light = LightSource(
    [-75000000, 0, -75000000],  # Position approximative du Soleil
    'color', [1, 1, 1],
    'parallel', 'point_at', [0, 0, 0]
)

earth = BasicEarth().get_povray_object()

cubesat = PrimitiveCubesat(
    position=[0,0,earth_radius + sat_altitude - relative_distance],
    rotation=[45,45,45],
    size=10,
    thickness=1
).get_cubesat()

# Scène
scene = Scene(
    camera,
    objects=[light, earth, cubesat],
    included=['metals.inc', 'textures.inc'],
)

# Rendu
output_folder = Path.home()
output_file = str(output_folder.joinpath("earth_and_cubesat_render.png"))
scene.render(output_file, width=1920, height=1080, tempfile='temp.pov', docker=True, resources_folder="/home/arnaud/workspace/5a/P2I_5A/P2i_POV_Ray/resources/")

print('Rendu terminé :', output_file)