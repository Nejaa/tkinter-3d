from __future__ import annotations
from tkinter import Canvas
from math import *
from typing import Optional


class GeometryOptions:
    def __init__(self):
        self.line_thickness = 1


geometry_options = GeometryOptions()


class Camera:
    def __init__(self, position: Vector, focal_length: float = -500):
        self.position = position.copy(label="camera")
        self.view_port = Vector(label="view_port", z=focal_length)
        # self.view_port = position.copy(label="view_port").translate(Vector(z=-focal_length))

    def translate(self, v: Vector):
        self.position.translate(v)

    def __str__(self):
        return "camera:\n    position={}\n    viewport offset={}".format(self.position, self.view_port)


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

    def rotate_y(self, angle, center: Vector) -> Vector:
        a = radians(angle) % pi

        # translate to origin
        orig_point = self - center

        # rotate
        new_x = orig_point.z * sin(a) + orig_point.x * cos(a)
        new_z = orig_point.z * cos(a) - orig_point.x * sin(a)

        # translate back
        self.x = new_x + center.x
        self.z = new_z + center.z
        return self

    def draw(self, canvas: Canvas):
        canvas.create_text(self.x, self.y, text=self.label)

    def project_to(self, camera: Camera):
        dx = self.x - camera.position.x
        dy = self.y - camera.position.y
        dz = self.z - camera.position.z

        if dz <= 0:
            self.visible = False
            return

        x = (camera.view_port.z / dz) * dx
        y = (camera.view_port.z / dz) * dy

        self.projection = Vector(self.label, x, y)
        self.visible = True

    def __add__(self, other: Vector) -> Vector:
        return Vector(
            x=self.x + other.x,
            y=self.y + other.y,
            z=self.z + other.z,
        )

    def __sub__(self, other: Vector) -> Vector:
        return Vector(
            x=self.x - other.x,
            y=self.y - other.y,
            z=self.z - other.z,
        )

    def __str__(self) -> str:
        return "({}, {}, {})".format(self.x, self.y, self.z)


class Line:
    def __init__(self, a: Vector, b: Vector):
        self.a = a
        self.b = b

    def draw(self, canvas: Canvas):
        if self.a.visible & self.b.visible:
            canvas.create_line(self.a.projection.x, self.a.projection.y, self.b.projection.x, self.b.projection.y,
                               width=geometry_options.line_thickness)


class Triangle:
    def __init__(self, a: Vector, b: Vector, c: Vector):
        self.a = a  # unused but who knows
        self.b = b  # unused but who knows
        self.c = c  # unused but who knows
        self.ab = Line(self.a, self.b)
        self.bc = Line(self.b, self.c)
        self.ca = Line(self.c, self.a)

    def draw(self, canvas: Canvas):
        self.ab.draw(canvas)
        self.bc.draw(canvas)
        self.ca.draw(canvas)


class Mesh:
    def __init__(self, *vertices: Vector):
        assert (len(vertices) % 3 == 0), "incorrect number of points for triangles"

        self.rotation = Vector()
        self.center = Vector()
        self.viewportPosition = Vector()
        self.vertices = vertices
        self.triangles = []
        i = 0
        while i < len(vertices):
            self.triangles.append(Triangle(self.vertices[i], self.vertices[i + 1], self.vertices[i + 2]))
            i += 3

    def set_center(self, center: Vector):
        self.center = center

    def draw(self, canvas: Canvas, debug=False):
        for triangle in self.triangles:
            triangle.draw(canvas)
        if debug:
            canvas.create_text(self.viewportPosition.x, self.viewportPosition.y,
                               text="Center = {}\nRotation = {}".format(self.center, self.rotation))
            for vertex in self.vertices:
                vertex.draw(canvas)

    def translate(self, v: Vector):
        self.center.translate(v)
        self.viewportPosition.translate(v)
        seen = []
        for vertex in self.vertices:
            if vertex in seen:
                continue
            vertex.translate(v)
            seen.append(vertex)

    def translate_projections(self, v: Vector):
        seen = []
        self.viewportPosition.translate(v)
        for vertex in self.vertices:
            if vertex in seen:
                continue
            vertex.projection.translate(v)
            seen.append(vertex)

    def rotate_y(self, angle: float, center: Optional[Vector] = None):
        center = self.center if center is None else center

        seen = []
        for vertex in self.vertices:
            if vertex in seen:
                continue
            vertex.rotate_y(angle, center)
            seen.append(vertex)

        self.rotation.y = (self.rotation.y + angle) % 360

    def project_to(self, camera: Camera):
        seen = []
        for vertex in self.vertices:
            if vertex in seen:
                continue
            vertex.project_to(camera=camera)
            seen.append(vertex)

        self.center.project_to(camera)
        self.viewportPosition = self.center.projection

    def copy(self, offset: Vector) -> Mesh:
        vertices = [p.copy() for p in self.vertices]
        m = Mesh(*vertices)
        m.set_center(self.center.copy())
        m.translate(offset)
        return m
