from __future__ import annotations

from geometry.mesh import Mesh


class Entity:
    def __init__(self, geometry: Mesh):
        self.geometry = geometry

    def copy(self) -> Entity:
        return Entity(self.geometry.copy())

    def build_global_positions(self):
        for vertex in self.geometry.vertices:
            vertex.move_to(vertex.translate(self.geometry.center))
        for triangle in self.geometry.triangles:
            triangle.center.move_to(triangle.center.translate(self.geometry.center))
