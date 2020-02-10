from geometry.mesh import Mesh


class Entity:
    def __init__(self, geometry: Mesh):
        self.geometry = geometry