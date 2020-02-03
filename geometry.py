from __future__ import annotations
from tkinter import Canvas
from math import *
from typing import Optional


class GeometryOptions:
    def __init__(self):
        self.line_thickness = 1


geometry_options = GeometryOptions()


class Camera:
    def __init__(self, position: Vector, focal_length: float = 500):
        self.position = position.copy(label="camera")
        self.rotation = Vector()
        self.rotation_rad = Vector()
        self.bearing = Vector(z=1)
        self.view_port = Vector(label="view_port", z=focal_length)

    def translate(self, v: Vector):
        self.position.translate(v)

    def rotate(self, rotation: Vector):
        self.rotation.x = (self.rotation.x - rotation.x) % 360
        self.rotation.y = (self.rotation.y + rotation.y) % 360
        self.rotation.z = (self.rotation.z + rotation.z) % 360
        self.rotation_rad.x = radians(self.rotation.x) % (2 * pi)
        self.rotation_rad.y = radians(self.rotation.y) % (2 * pi)
        self.rotation_rad.z = radians(self.rotation.z) % (2 * pi)
        # Invert components for some reason
        self.bearing = self.bearing.rotate(angle=Vector(x=-rotation.x, y=-rotation.y, z=rotation.z))

    def __str__(self):
        return "camera:\n" \
               "    position={}\n" \
               "    rotation={}\n" \
               "    rotation_rad={}\n" \
               "    bearing={}\n" \
               "    viewport offset={}".format(self.position, self.rotation, self.rotation_rad.copy() / pi,
                                               self.bearing,
                                               self.view_port)


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
        canvas.create_text(self.x, self.y, text=self.label)

    def project_to(self, camera: Camera):
        cx = cos(camera.rotation_rad.x)
        sx = sin(camera.rotation_rad.x)
        cy = cos(camera.rotation_rad.y)
        sy = sin(camera.rotation_rad.y)
        cz = cos(camera.rotation_rad.z)
        sz = sin(camera.rotation_rad.z)

        delta = self - camera.position

        if delta.dot(camera.bearing) <= 0.0:
            self.visible = False
            return

        d_x = cy * (sz * delta.y + cz * delta.x) - sy * delta.z
        d_y = sx * (cy * delta.z + sy * (sz * delta.y + cz * delta.x)) + cx * (cz * delta.y - sz * delta.x)
        d_z = cx * (cy * delta.z + sy * (sz * delta.y + cz * delta.x)) - sx * (cz * delta.y - sz * delta.x)

        x = (camera.view_port.z / d_z) * d_x
        y = (camera.view_port.z / d_z) * d_y

        self.projection = Vector(self.label, x, -y)
        self.visible = True

    def dot(self, other: Vector) -> float:
        return self.x * other.x + self.y * other.y + self.z * other.z

    def __invert__(self) -> Vector:
        return Vector(x=-self.x, y=-self.y, z=-self.z)

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

    def __truediv__(self, div: float) -> Vector:
        return Vector(x=self.x / div, y=self.y / div, z=self.z / div)

    def __str__(self) -> str:
        return "({:.2f}, {:.2f}, {:.2f})".format(self.x, self.y, self.z)


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

    def rotate_x(self, angle: float, center: Optional[Vector] = None):
        center = self.center if center is None else center

        seen = []
        for vertex in self.vertices:
            if vertex in seen:
                continue
            vertex.rotate_x(angle, center)
            seen.append(vertex)

        self.rotation.x = (self.rotation.x + angle) % 360

    def rotate_y(self, angle: float, center: Optional[Vector] = None):
        center = self.center if center is None else center

        seen = []
        for vertex in self.vertices:
            if vertex in seen:
                continue
            vertex.rotate_y(angle, center)
            seen.append(vertex)

        self.rotation.y = (self.rotation.y + angle) % 360

    def rotate_z(self, angle: float, center: Optional[Vector] = None):
        center = self.center if center is None else center

        seen = []
        for vertex in self.vertices:
            if vertex in seen:
                continue
            vertex.rotate_z(angle, center)
            seen.append(vertex)

        self.rotation.z = (self.rotation.z + angle) % 360

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
