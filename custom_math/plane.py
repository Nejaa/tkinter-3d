from typing import List

from custom_math.vector3d import Vector3D
from geometry.line import Line
from geometry.triangle import Triangle


class Plane:
    def __init__(self, position: Vector3D, normal: Vector3D):
        self.position = position
        self.normal = normal.normalize()

    def intersect(self, line: Line) -> Vector3D:
        plane_d = -self.normal.dot(self.position)

        ad = line.a.dot(self.normal)
        bd = line.b.dot(self.normal)

        t = (-plane_d - ad) / (bd-ad)

        line_start_end = line.b - line.a
        line_to_intersect = line_start_end * t

        intersection = line.a + line_to_intersect

        return intersection

    def dist(self, point: Vector3D) -> float:
        plane_d = self.normal.dot(self.position)
        return self.normal.x * point.x + self.normal.y * point.y + self.normal.z * point.z - plane_d

    def clip_triangle(self, triangle: Triangle) -> List[Triangle]:

        inside_points = []
        outside_points = []

        if self.dist(triangle.a) >= 0:
            inside_points.append(triangle.a)
        else:
            outside_points.append(triangle.a)
        if self.dist(triangle.b) >= 0:
            inside_points.append(triangle.b)
        else:
            outside_points.append(triangle.b)
        if self.dist(triangle.c) >= 0:
            inside_points.append(triangle.c)
        else:
            outside_points.append(triangle.c)

        inside_count = len(inside_points)
        if inside_count == 0:
            return []
        if inside_count == 3:
            return [triangle]

        outside_count = len(outside_points)
        if inside_count == 1 and outside_count == 2:
            return [
                Triangle(
                    a=inside_points[0],
                    b=self.intersect(line=Line(a=inside_points[0], b=outside_points[0])),
                    c=self.intersect(line=Line(a=inside_points[0], b=outside_points[1]))
                )
            ]

        if inside_count == 2 and outside_count == 1:
            t1 = Triangle(a=inside_points[0],
                          b=inside_points[1],
                          c=self.intersect(line=Line(a=inside_points[0], b=outside_points[0])))

            t2 = Triangle(a=inside_points[1],
                          b=t1.c,
                          c=self.intersect(line=Line(a=inside_points[1], b=outside_points[0])))
            return [
                t1,
                t2
            ]

        return []
