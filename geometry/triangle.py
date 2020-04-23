from __future__ import annotations

from custom_math.vector3d import Vector3D
from geometry.line import Line


class Triangle:
    def __init__(self, a: Vector3D, b: Vector3D, c: Vector3D):
        self.a = a
        self.b = b
        self.c = c
        self.ab = Line(self.a, self.b)
        self.bc = Line(self.b, self.c)
        self.ca = Line(self.c, self.a)
        self.debugNormal: Vector3D = None
        self.projectedNormal: Vector3D = None
        self.center = Vector3D(
            x=self.a.x + self.b.x + self.c.x,
            y=self.a.y + self.b.y + self.c.y,
            z=self.a.z + self.b.z + self.c.z,
        ) / 3

    def copy(self) -> Triangle:
        triangle = Triangle(a=self.a.copy(), b=self.b.copy(), c=self.c.copy(), )
        triangle.debugNormal = self.debugNormal
        return triangle

    def normal(self) -> Vector3D:
        v1 = self.b - self.a
        v2 = self.c - self.a
        cross = v1.cross(v2)
        cross = cross.normalize()
        return cross

