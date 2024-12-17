"""Definition of a really primitive Cubesat."""

from vapory import Texture, Pigment, Finish, Box, Union, POVRayElement


class PrimitiveCubesat(POVRayElement):
    """
    Représente un CubeSat avec des panneaux solaires, des faces en aluminium et des faces dorées.
    """

    def __init__(self, position: list[float], rotation: list[float], size: float = 0.0001, thickness: float = 0.00001):
        """
        Constructeur de la classe PrimitiveCubesat.

        :param position: Position absolue du CubeSat [x, y, z].
        :param rotation: Rotation du CubeSat sur les axes [x, y, z] (en degrés).
        :param size: Taille du CubeSat (cm).
        :param thickness: Épaisseur des faces du CubeSat (cm).
        """
        self.position = position
        self.rotation = rotation
        self.size = size
        self.thickness = thickness
        self.cubesat_model = self.get_cubesat()

    def _create_solar_panel_texture(self) -> Texture:
        """
        Crée et retourne la texture pour les panneaux solaires.

        :return: Texture des panneaux solaires.
        """
        return Texture(
            Pigment('color', [0.2, 0.2, 0.8]),
            Finish('diffuse', 0.8, 'ambient', 0.2, 'specular', 0.3)
        )

    def _create_material_texture(self, material: str) -> Texture:
        """
        Crée et retourne une texture de matériau.

        :param material: Nom du matériau.
        :return: Texture pour le matériau spécifié.
        """
        return Texture(material)

    def get_cubesat(self) -> Union:
        """
        Crée et retourne le modèle du CubeSat.

        :return: Modèle du CubeSat.
        """
        solar_panel_texture = self._create_solar_panel_texture()

        cubesat_faces = Union(
            # Faces avec panneaux solaires (Z+ et Z-)
            Box([-self.size*1e-5, -self.size*1e-5, self.size*1e-5 - self.thickness*1e-5],
                [self.size*1e-5, self.size*1e-5, self.size*1e-5],
                solar_panel_texture),
            Box([-self.size*1e-5, -self.size*1e-5, -self.size*1e-5],
                [self.size*1e-5, self.size*1e-5, -self.size*1e-5 + self.thickness*1e-5],
                solar_panel_texture),
            # Faces en aluminium (X+ et X-)
            Box([self.size*1e-5 - self.thickness*1e-5, -self.size*1e-5, -self.size*1e-5],
                [self.size*1e-5, self.size*1e-5, self.size*1e-5],
                self._create_material_texture('Brushed_Aluminum')),
            Box([-self.size*1e-5, -self.size*1e-5, -self.size*1e-5],
                [-self.size*1e-5 + self.thickness*1e-5, self.size*1e-5, self.size*1e-5],
                self._create_material_texture('Brushed_Aluminum')),
            # Faces dorées (Y+ et Y-)
            Box([-self.size*1e-5, self.size*1e-5 - self.thickness*1e-5, -self.size*1e-5],
                [self.size*1e-5, self.size*1e-5, self.size*1e-5],
                self._create_material_texture('T_Gold_1A')),
            Box([-self.size*1e-5, -self.size*1e-5, -self.size*1e-5],
                [self.size*1e-5, -self.size*1e-5 + self.thickness*1e-5, self.size*1e-5],
                self._create_material_texture('T_Gold_1A'))
        )

        # Ajouter la rotation et la position
        return cubesat_faces.add_args([
            'rotate', self.rotation,
            'translate', self.position
        ])