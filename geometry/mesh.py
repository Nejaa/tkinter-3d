from __future__ import annotations

from tkinter import Canvas
from typing import Optional

from geometry.Triangle import Triangle
from geometry.camera import Camera
from geometry.vector import Vector
from geometry.quaternion import Quaternion


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

    def rotate(self, rotation: Quaternion):
        seen = []
        for vertex in self.vertices:
            if vertex in seen:
                continue
            v = rotation.rotate(vertex)
            vertex.move_to(v)
            seen.append(vertex)

    def project_to(self, camera: Camera):
        seen = []
        for vertex in self.vertices:
            if vertex in seen:
                continue
            camera.project(point=vertex, mesh_position=self.center)
            seen.append(vertex)

        camera.project(point=self.viewportPosition, mesh_position=self.center)

    def copy(self, offset: Vector) -> Mesh:
        vertices = [p.copy() for p in self.vertices]
        m = Mesh(*vertices)
        m.set_center(self.center.copy())
        m.translate(offset)
        return m
