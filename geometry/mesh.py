from __future__ import annotations

import re
from tkinter import Canvas
from typing import List, Set

from geometry.triangle import Triangle
from custom_math.quaternion import Quaternion
from custom_math.vector3d import Vector3D


class Mesh:
    def __init__(self, *triangles: Triangle):
        self.rotation = Vector3D()
        self.center = Vector3D()
        self.viewportPosition = Vector3D()
        self.triangles: List[Triangle] = []
        self.vertices: Set[Vector3D] = set()
        self.set_triangles(*triangles)

    @staticmethod
    def from_vertices(*vertices: Vector3D) -> Mesh:
        assert (len(vertices) % 3 == 0), "incorrect number of points for triangles build"
        triangles = []
        i = 0
        while i < len(vertices):
            triangles.append(Triangle(vertices[i], vertices[i + 1], vertices[i + 2]))
            i += 3

        return Mesh(*triangles)

    def set_triangles(self, *triangles: Triangle):
        self.triangles = triangles
        self.vertices.clear()
        vertexMap = {}
        for triangle in self.triangles:
            if triangle.a not in vertexMap:
                self.vertices.add(triangle.a)
                vertexMap[triangle.a] = triangle.a
            else:
                knownVertex = vertexMap[triangle.a]
                triangle.a = knownVertex

            if triangle.b not in vertexMap:
                self.vertices.add(triangle.b)
                vertexMap[triangle.b] = triangle.b
            else:
                knownVertex = vertexMap[triangle.b]
                triangle.b = knownVertex

            if triangle.c not in vertexMap:
                self.vertices.add(triangle.c)
                vertexMap[triangle.c] = triangle.c
            else:
                knownVertex = vertexMap[triangle.c]
                triangle.c = knownVertex
            triangle.build_lines()

    def set_center(self, center: Vector3D):
        self.center = center

    def translate(self, v: Vector3D) -> Mesh:
        self.center = self.center.translate(v)
        return self

    def rotate(self, rotation: Quaternion) -> Mesh:
        for vertex in self.vertices:
            v = rotation.rotate(vertex)
            vertex.move_to(v)
        return self

    def scale(self, scale_factor: float) -> Mesh:
        for vertex in self.vertices:
            v = vertex * scale_factor
            vertex.move_to(v)
        return self

    def copy(self, offset: Vector3D = Vector3D()) -> Mesh:
        triangles = [t.copy() for t in self.triangles]
        m = Mesh(*triangles)
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
                vertex = Vector3D(x=float(groups[0]), y=float(groups[1]), z=float(groups[2]))
                vertices.append(vertex)
            elif line_type == "s":
                pass  # Smooth shading ignored
            elif line_type == "f":
                groups = triangle_regex.search(line).groups()
                triangles.append(Triangle(a=vertices[int(groups[0]) - 1],
                                          b=vertices[int(groups[1]) - 1],
                                          c=vertices[int(groups[2]) - 1]))
            else:
                print("ignored unknown format line {}".format(line))

        return Mesh(*triangles)
