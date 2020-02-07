from __future__ import annotations
from math import radians, sin, cos, sqrt, atan2, asin, pi, fabs, copysign

from geometry.vector import Vector


class Quaternion:
    def __init__(self, w: float, axis: Vector):
        self.w = w
        self.axis = axis

    def rotate(self, v: Vector) -> Vector:
        q = self
        p = Quaternion(0, v)
        r = q * p * q.conjugate()
        return r.axis

    def det(self) -> float:
        sq_axis = self.axis ** 2
        return sqrt(self.w ** 2 + sq_axis.x + sq_axis.y + sq_axis.z)

    def conjugate(self) -> Quaternion:
        return Quaternion(w=self.w, axis=-self.axis)

    def euler_angles(self) -> Vector:
        angles = Vector()

        sinr_cosp = 2 * (self.w * self.axis.x + self.axis.y * self.axis.z)
        cosr_cosp = 1 - 2 * (self.axis.x ** 2 + self.axis.y ** 2)

        # roll (x-axis rotation)
        angles.x = atan2(sinr_cosp, cosr_cosp)

        sinp = 2 * (self.w * self.axis.y - self.axis.z * self.axis.x)
        if fabs(sinp) >= 1:
            angles.y = copysign(pi / 2, sinp)
        else:
            angles.y = asin(sinp)

        siny_cosp = 2 * (self.w * self.axis.z + self.axis.x * self.axis.y)
        cosy_cosp = 1 - 2 * (self.axis.y ** 2 + self.axis.z ** 2)
        angles.z = atan2(siny_cosp, cosy_cosp)

        return angles

    # def euler_angles(self) -> Vector:
    #     test = self.axis.x * self.axis.y + self.axis.z * self.w
    #     if (test > 0.499) | (test < -0.499):  # singularity at north or south pole
    #         heading = 2 * atan2(self.axis.x, self.w)
    #         attitude = pi / 2
    #         bank = 0
    #         if test < 0:
    #             heading = -heading
    #             attitude = -attitude
    #
    #         return Vector(x=bank, y=heading, z=attitude)
    #
    #     sqx = self.axis.x ** 2
    #     sqy = self.axis.y ** 2
    #     sqz = self.axis.z ** 2
    #     heading = atan2(2 * self.axis.y * self.w - 2 * self.axis.x * self.axis.z, 1 - 2 * sqy - 2 * sqz)
    #     attitude = asin(2 * test)
    #     bank = atan2(2 * self.axis.x * self.w - 2 * self.axis.y * self.axis.z, 1 - 2 * sqx - 2 * sqz)
    #
    #     return Vector(x=bank, y=heading, z=attitude)

    @staticmethod
    def axis_angle(axis: Vector, angle: float) -> Quaternion:
        v = axis.normalize()
        rad = radians(angle / 2)
        s = sin(rad)
        w = cos(rad)
        vs = v * s

        return Quaternion(w, vs)

    @staticmethod
    def identity() -> Quaternion:
        return Quaternion(1, Vector())

    def __mul__(self, other: Quaternion) -> Quaternion:
        t0 = (other.w * self.w - other.axis.x * self.axis.x - other.axis.y * self.axis.y - other.axis.z * self.axis.z)
        t1 = (other.w * self.axis.x + other.axis.x * self.w - other.axis.y * self.axis.z + other.axis.z * self.axis.y)
        t2 = (other.w * self.axis.y + other.axis.x * self.axis.z + other.axis.y * self.w - other.axis.z * self.axis.x)
        t3 = (other.w * self.axis.z - other.axis.x * self.axis.y + other.axis.y * self.axis.x + other.axis.z * self.w)
        return Quaternion(t0, Vector(x=t1, y=t2, z=t3))

    def __str__(self) -> str:
        return "({:.5f}, {:.5f}, {:.5f}, {:.5f})".format(self.w, self.axis.x, self.axis.y, self.axis.z)
