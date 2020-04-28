from __future__ import annotations

from math import degrees, sqrt
from typing import Optional

from custom_math.matrix import Matrix


class Vector3D:
    def __init__(self, label="", x: float = 0.0, y: float = 0.0, z: float = 0.0):
        self.label = label
        self.x = x
        self.y = y
        self.z = z
        self.w = 1
        self.debug_txt = self.__str__()

    def copy(self, label: Optional[str] = None) -> Vector3D:
        v = Vector3D(label=self.label if label is None else label, x=self.x, y=self.y, z=self.z)
        v.w = self.w
        return v

    def translate(self, v: Vector3D) -> Vector3D:
        newV = self.copy()
        newV.x += v.x
        newV.y += v.y
        newV.z += v.z
        return newV

    def dot(self, other: Vector3D) -> float:
        return self.x * other.x + self.y * other.y + self.z * other.z

    def cross(self, other: Vector3D) -> Vector3D:
        return Vector3D(
            x=self.y * other.z - self.z * other.y,
            y=self.z * other.x - self.x * other.z,
            z=self.x * other.y - self.y * other.x,
        )

    def magnitude(self) -> float:
        return sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)

    def normalize(self) -> Vector3D:
        mag = self.magnitude()
        if mag == 0:
            return Vector3D()
        return self / mag

    def move_to(self, v: Vector3D):
        self.x = v.x
        self.y = v.y
        self.z = v.z

    def to_degree(self):
        return Vector3D(x=degrees(self.x), y=degrees(self.y), z=degrees(self.z))

    def __invert__(self) -> Vector3D:
        return Vector3D(x=-self.x, y=-self.y, z=-self.z)

    def __add__(self, other: Vector3D) -> Vector3D:
        return Vector3D(
            label=self.label,
            x=self.x + other.x,
            y=self.y + other.y,
            z=self.z + other.z,
        )

    def __pow__(self, power, modulo=None) -> Vector3D:
        return Vector3D(x=self.x ** power, y=self.y ** power, z=self.z ** power)

    def __sub__(self, other: Vector3D) -> Vector3D:
        return Vector3D(
            label=self.label,
            x=self.x - other.x,
            y=self.y - other.y,
            z=self.z - other.z,
        )

    def __neg__(self) -> Vector3D:
        return Vector3D() - self

    def __mul__(self, mul: float):
        return Vector3D(x=self.x * mul, y=self.y * mul, z=self.z * mul)

    def __truediv__(self, div: float) -> Vector3D:
        return Vector3D(x=self.x / div, y=self.y / div, z=self.z / div)

    def __str__(self) -> str:
        return "({:.2f}, {:.2f}, {:.2f})".format(self.x, self.y, self.z)

    def __hash__(self):
        return hash((self.x, self.y, self.z))

    def __eq__(self, other: Vector3D):
        return self.x == other.x and self.y == other.y and self.z == other.z

    def is_same(self, other: Vector3D) -> bool:
        return self.x == other.x and self.y == other.y and self.z == other.z

    @staticmethod
    def up(screen_space=False) -> Vector3D:
        v = Vector3D(y=1)
        if screen_space:
            v = Vector3D(y=-1)
        return v

    @staticmethod
    def down(screen_space=False) -> Vector3D:
        v = Vector3D(y=-1)
        if screen_space:
            v = Vector3D(y=1)
        return v

    @staticmethod
    def left() -> Vector3D:
        return Vector3D(x=-1)

    @staticmethod
    def right() -> Vector3D:
        return Vector3D(x=1)

    @staticmethod
    def forward() -> Vector3D:
        return Vector3D(z=1)

    @staticmethod
    def backward() -> Vector3D:
        return Vector3D(z=-1)

    def to_matrix(self) -> Matrix:
        return Matrix([[self.x], [self.y], [self.z], [self.w]])
