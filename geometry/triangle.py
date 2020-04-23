from __future__ import annotations

from geometry.line import Line
from custom_math.vector3d import Vector3D


class Triangle:
    def __init__(self, a: Vector3D, b: Vector3D, c: Vector3D):
        self.a = a
        self.b = b
        self.c = c
        self.ab = Line(self.a, self.b)
        self.bc = Line(self.b, self.c)
        self.ca = Line(self.c, self.a)

    def copy(self) -> Triangle:
        return Triangle(
            a=self.a.copy(),
            b=self.b.copy(),
            c=self.c.copy(),
        )
