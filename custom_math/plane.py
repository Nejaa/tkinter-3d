from custom_math.vector3d import Vector3D
from geometry.line import Line


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
