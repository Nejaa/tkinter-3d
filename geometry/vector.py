from __future__ import annotations

from math import radians, sin, cos
from tkinter import Canvas
from typing import Optional


class Vector:
    def __init__(self, label="", x: float = 0.0, y: float = 0.0, z: float = 0.0):
        self.label = label
        self.x = x
        self.y = y
        self.z = z
        self.projection = self
        self.visible = False

    def copy(self, label: Optional[str] = None) -> Vector:
        return Vector(label=self.label if label is None else label, x=self.x, y=self.y, z=self.z)

    def translate(self, v: Vector) -> Vector:
        self.x += v.x
        self.y += v.y
        self.z += v.z
        return self

    def rotate(self, angle: Vector, center: Vector = None):
        center = Vector() if center is None else center
        temp = self.rotate_x(angle.x, center)
        temp = temp.rotate_y(angle.y, center)
        temp = temp.rotate_z(angle.z, center)
        return temp

    def rotate_x(self, angle, center: Vector) -> Vector:
        a = radians(angle)

        # translate to origin
        orig_point = self - center

        # rotate
        new_y = orig_point.z * sin(a) + orig_point.y * cos(a)
        new_z = orig_point.z * cos(a) - orig_point.y * sin(a)

        # translate back
        self.y = new_y + center.y
        self.z = new_z + center.z
        return self

    def rotate_y(self, angle, center: Vector) -> Vector:
        a = radians(-angle)

        # translate to origin
        orig_point = self - center

        # rotate
        new_x = orig_point.z * sin(a) + orig_point.x * cos(a)
        new_z = orig_point.z * cos(a) - orig_point.x * sin(a)

        # translate back
        self.x = new_x + center.x
        self.z = new_z + center.z
        return self

    def rotate_z(self, angle, center: Vector) -> Vector:
        a = radians(-angle)

        # translate to origin
        orig_point = self - center

        # rotate
        new_x = orig_point.y * sin(a) + orig_point.x * cos(a)
        new_y = orig_point.y * cos(a) - orig_point.x * sin(a)

        # translate back
        self.x = new_x + center.x
        self.y = new_y + center.y
        return self

    def draw(self, canvas: Canvas):
        canvas.create_text(self.projection.x, self.projection.y, text=self.label)

    def dot(self, other: Vector) -> float:
        return self.x * other.x + self.y * other.y + self.z * other.z

    def __invert__(self) -> Vector:
        return Vector(x=-self.x, y=-self.y, z=-self.z)

    def __add__(self, other: Vector) -> Vector:
        return Vector(
            label=self.label,
            x=self.x + other.x,
            y=self.y + other.y,
            z=self.z + other.z,
        )

    def __sub__(self, other: Vector) -> Vector:
        return Vector(
            label=self.label,
            x=self.x - other.x,
            y=self.y - other.y,
            z=self.z - other.z,
        )

    def __truediv__(self, div: float) -> Vector:
        return Vector(x=self.x / div, y=self.y / div, z=self.z / div)

    def __str__(self) -> str:
        return "({:.2f}, {:.2f}, {:.2f})".format(self.x, self.y, self.z)