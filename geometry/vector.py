from __future__ import annotations

from math import degrees, sqrt
from tkinter import Canvas
from typing import Optional


class Vector:
    def __init__(self, label="", x: float = 0.0, y: float = 0.0, z: float = 0.0):
        self.label = label
        self.x = x
        self.y = y
        self.z = z
        self.d = 0
        self.projection = self
        self.visible = False

    def copy(self, label: Optional[str] = None) -> Vector:
        return Vector(label=self.label if label is None else label, x=self.x, y=self.y, z=self.z)

    def translate(self, v: Vector) -> Vector:
        self.x += v.x
        self.y += v.y
        self.z += v.z
        return self

    def draw(self, canvas: Canvas):
        canvas.create_text(self.projection.x, self.projection.y, text=self.label)
        canvas.create_text(self.projection.x, self.projection.y + 10, text="{:.2}".format(self.projection.d))

    def dot(self, other: Vector) -> float:
        return self.x * other.x + self.y * other.y + self.z * other.z

    def magnitude(self) -> float:
        return sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)

    def normalize(self) -> Vector:
        mag = self.magnitude()
        return self / mag

    def move_to(self, v: Vector):
        self.x = v.x
        self.y = v.y
        self.z = v.z

    def to_degree(self):
        return Vector(x=degrees(self.x), y=degrees(self.y), z=degrees(self.z))

    def __invert__(self) -> Vector:
        return Vector(x=-self.x, y=-self.y, z=-self.z)

    def __add__(self, other: Vector) -> Vector:
        return Vector(
            label=self.label,
            x=self.x + other.x,
            y=self.y + other.y,
            z=self.z + other.z,
        )

    def __pow__(self, power, modulo=None) -> Vector:
        return Vector(x=self.x ** power, y=self.y ** power, z=self.z ** power)

    def __sub__(self, other: Vector) -> Vector:
        return Vector(
            label=self.label,
            x=self.x - other.x,
            y=self.y - other.y,
            z=self.z - other.z,
        )

    def __neg__(self) -> Vector:
        return Vector() - self

    def __mul__(self, mul: float):
        return Vector(x=self.x * mul, y=self.y * mul, z=self.z * mul)

    def __truediv__(self, div: float) -> Vector:
        return Vector(x=self.x / div, y=self.y / div, z=self.z / div)

    def __str__(self) -> str:
        return "({:.2f}, {:.2f}, {:.2f})".format(self.x, self.y, self.z)

    def is_same(self, other: Vector) -> bool:
        return self.x == other.x and self.y == other.y and self.z == other.z
