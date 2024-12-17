from pathlib import Path
from vapory import BumpMap, Normal, Camera, Object, LightSource, Sphere, Texture, Pigment, Finish, Scene, ImageMap, Box, Union,PigmentMap, Background

# Définir les constantes
earth_radius = 6378.0  # Rayon de la Terre en km
sat_altitude = 10000.0  # Altitude du satellite en km
relative_distance = 5.0  # Distance relative pour positionner le CubeSat
fov_degree = 60  # Champ de vision en degrés
cube_sat_size = 0.0001  # Taille du CubeSat en km (échelle exagérée)
cube_sat_thk = 0.00001  # Épaisseur des faces du CubeSat

# Chemin des images
image_folder = Path(__file__).parents[2].joinpath('resources/images/')
print(f"Chemin des images : {image_folder}")

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
    [75000000, 0, 75000000],  # Position approximative du Soleil
    'color', [1, 1, 1],
    'parallel', 'point_at', [0, 0, 0]
)

# Définition des pigments et textures
earth_pigment = Pigment(
    ImageMap(
        "tiff", f"\"{str('/resources/images/earth_color_43K.tif')}\"",
        'map_type', 1, 'interpolate', 2,
    ),
        # # 'gradient', 'x',
        # 'scale', [earth_radius * 2, earth_radius * 2, earth_radius * 2],
)

earth_normal = Normal(
    BumpMap( 
        f"\"{str('/resources/images/topography_21K.png')}\"",
        "map_type", 1,
        "interpolate", 2,
        "bump_size", 0.05
    )
)
earth_texture = Texture(
    earth_pigment,
    Finish('diffuse', 0.8, 'ambient', 0, 'specular', 0.2, 'roughness', 0.05),
    earth_normal
)

# Sphère représentant la Terre
earth = Object(
    Sphere(
        [0, 0, 0], earth_radius
    ),
    earth_texture,
    'rotate', [0, 25, 0]
)
# Définition du pigment des nuages
clouds_pigment = Pigment(
    ImageMap(
        "tiff", f"\"{str('/resources/images/earth_clouds_43K.tif')}\"",
        'map_type', 1, 'interpolate', 2,
        'transmit', 'all', 0.8
    )
)

# Nuages sur une sphère légèrement plus grande
clouds = Object(
    Sphere(
    [0, 0, 0], earth_radius + 10,
    ),
    Texture(
        clouds_pigment,
        Finish('diffuse', 0.7, 'ambient', 0.0, 'specular', 0.2)
    ),
    'hollow'
)

# Définition du CubeSat
solar_panel_texture = Texture(
    Pigment('color', [0.2, 0.2, 0.8]),
    Finish('diffuse', 0.8, 'ambient', 0.2, 'specular', 0.3)
)

cubesat_faces = Union(
    # Face avec panneaux solaires (Z+ et Z-)
    Box([-cube_sat_size, -cube_sat_size, cube_sat_size - cube_sat_thk],
        [cube_sat_size, cube_sat_size, cube_sat_size],
        solar_panel_texture),
    Box([-cube_sat_size, -cube_sat_size, -cube_sat_size],
        [cube_sat_size, cube_sat_size, -cube_sat_size + cube_sat_thk],
        solar_panel_texture),
    # Face en aluminium (X+ et X-)
    Box([cube_sat_size - cube_sat_thk, -cube_sat_size, -cube_sat_size],
        [cube_sat_size, cube_sat_size, cube_sat_size],
        Texture('Brushed_Aluminum')),
    Box([-cube_sat_size, -cube_sat_size, -cube_sat_size],
        [-cube_sat_size + cube_sat_thk, cube_sat_size, cube_sat_size],
        Texture('Brushed_Aluminum')),
    # Face dorée (Y+ et Y-)
    Box([-cube_sat_size, cube_sat_size - cube_sat_thk, -cube_sat_size],
        [cube_sat_size, cube_sat_size, cube_sat_size],
        Texture('T_Gold_1A')),
    Box([-cube_sat_size, -cube_sat_size, -cube_sat_size],
        [cube_sat_size, -cube_sat_size + cube_sat_thk, cube_sat_size],
        Texture('T_Gold_1A'))
)

cubesat = cubesat_faces.add_args(['rotate', [45, 45, 45], 'translate', [0, 0, earth_radius + sat_altitude - relative_distance]])

# Scène
scene = Scene(
    camera,
    objects=[light, earth, clouds, cubesat],
    included=['metals.inc', 'textures.inc'],
)

# Rendu
output_folder = Path.home()
output_file = str(output_folder.joinpath("earth_and_cubesat_render.png"))
scene.render(output_file, width=1920, height=1080, tempfile='temp.pov', docker=True, resources_folder="/home/arnaud/workspace/5a/P2I_5A/P2i_POV_Ray/resources/")

print('Rendu terminé :', output_file)