from __future__ import annotations

from geometry.mesh import Mesh


class Entity:
    def __init__(self, geometry: Mesh):
        self.geometry = geometry

    def copy(self) -> Entity:
        return Entity(self.geometry.copy())
