from __future__ import annotations

import re
from tkinter import Canvas

from geometry.Triangle import Triangle
from geometry.camera import Camera
from geometry.quaternion import Quaternion
from geometry.vector import Vector


class Mesh:
    def __init__(self, *triangles: Vector):
        assert (len(triangles) % 3 == 0), "incorrect number of points for triangles"

        self.rotation = Vector()
        self.center = Vector()
        self.viewportPosition = Vector()
        self.vertices = triangles
        self.triangles = []
        i = 0
        while i < len(triangles):
            self.triangles.append(Triangle(self.vertices[i], self.vertices[i + 1], self.vertices[i + 2]))
            i += 3

    def set_center(self, center: Vector):
        self.center = center

    def draw(self, canvas: Canvas, debug=False):
        for triangle in self.triangles:
            triangle.draw(canvas)
        if debug:
            canvas.create_text(self.viewportPosition.projection.x, self.viewportPosition.projection.y,
                               text="Center = {}\nRotation = {}".format(self.center, self.rotation))
            for vertex in self.vertices:
                vertex.draw(canvas)

    def translate(self, v: Vector):
        self.center.translate(v)

    def translate_projections(self, v: Vector):
        seen = []
        self.viewportPosition.projection.translate(v)
        for vertex in self.vertices:
            if vertex in seen:
                continue
            vertex.projection.translate(v)
            seen.append(vertex)

    def rotate(self, rotation: Quaternion) -> Mesh:
        seen = []
        for vertex in self.vertices:
            if vertex in seen:
                continue
            v = rotation.rotate(vertex)
            vertex.move_to(v)
            seen.append(vertex)
        return self

    def scale(self, scale_factor: float) -> Mesh:
        seen = []
        for vertex in self.vertices:
            if vertex in seen:
                continue
            v = vertex * scale_factor
            vertex.move_to(v)
            seen.append(vertex)
        return self

    def project_to(self, camera: Camera):
        seen = []
        for vertex in self.vertices:
            if vertex in seen:
                continue
            camera.project(point=vertex, mesh_position=self.center)
            seen.append(vertex)

        camera.project(point=self.viewportPosition, mesh_position=self.center)

    def copy(self, offset: Vector = Vector()) -> Mesh:
        vertices = [p.copy() for p in self.vertices]
        m = Mesh(*vertices)
        m.set_center(self.center.copy())
        m.translate(offset)
        return m

    @staticmethod
    def import_from(file_path: str) -> Mesh:
        f = open(file_path, "r")

        vertex_regex = re.compile("v\\s(-?[.0-9]+)\\s(-?[.0-9]+)\\s(-?[.0-9]+)")
        triangle_regex = re.compile("f\\s(\\d+)\\s(\\d+)\\s(\\d+)")

        vertices = []
        triangles = []
        lines = f.readlines()
        for line in lines:
            line_type = line[0]
            if line_type == "#":
                continue  # line is comment
            elif line_type == "o":
                pass  # mesh name ignored
            elif line_type == "v":
                groups = vertex_regex.search(line).groups()
                vertex = Vector(x=float(groups[0]), y=float(groups[1]), z=float(groups[2]))
                vertices.append(vertex)
            elif line_type == "s":
                pass  # Smooth shading ignored
            elif line_type == "f":
                groups = triangle_regex.search(line).groups()
                triangles.append(vertices[int(groups[0])-1])
                triangles.append(vertices[int(groups[1])-1])
                triangles.append(vertices[int(groups[2])-1])
            else:
                print("ignored unknown format line {}".format(line))

        return Mesh(*triangles)
