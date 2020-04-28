from __future__ import annotations

from math import radians, sin, cos, sqrt, atan2, asin, pi, fabs, copysign

from custom_math.matrix import Matrix
from custom_math.vector3d import Vector3D


class Quaternion:
    def __init__(self, w: float, axis: Vector3D):
        self.w = w
        self.axis = axis

    def rotate(self, v: Vector3D) -> Vector3D:
        q = self
        p = Quaternion(0, v)
        r = q * p * q.conjugate()
        return r.axis

    def det(self) -> float:
        sq_axis = self.axis ** 2
        return sqrt(self.w ** 2 + sq_axis.x + sq_axis.y + sq_axis.z)

    def conjugate(self) -> Quaternion:
        return Quaternion(w=self.w, axis=-self.axis)

    def euler_angles(self) -> Vector3D:
        angles = Vector3D()

        sinr_cosp = 2 * (self.w * self.axis.x + self.axis.y * self.axis.z)
        cosr_cosp = 1 - 2 * (self.axis.x ** 2 + self.axis.y ** 2)

        # roll (x-axis rotation)
        angles.x = atan2(sinr_cosp, cosr_cosp)

        # pitch
        sinp = 2 * (self.w * self.axis.y - self.axis.z * self.axis.x)
        if fabs(sinp) >= 1:
            angles.y = copysign(pi / 2, sinp)
        else:
            angles.y = asin(sinp)

        # yaw
        siny_cosp = 2 * (self.w * self.axis.z + self.axis.x * self.axis.y)
        cosy_cosp = 1 - 2 * (self.axis.y ** 2 + self.axis.z ** 2)
        angles.z = atan2(siny_cosp, cosy_cosp)

        return angles

    def to_matrix(self) -> Matrix:
        x = self.axis.x
        y = self.axis.y
        z = self.axis.z
        w = self.w
        xx = x * x
        xy = x * y
        xz = x * z
        xw = x * w
        yy = y * y
        yz = y * z
        yw = y * w
        zz = z * z
        zw = z * w

        return Matrix([
            [1 - 2 * (yy + zz), 2 * (xy - zw), 2 * (xz + yw), 0],
            [2 * (xy + zw), 1 - 2 * (xx + zz), 2 * (yz - xw), 0],
            [2 * (xz - yw), 2 * (yz + xw), 1 - 2 * (xx + yy), 0],
            [0, 0, 0, 1],
        ])

    @staticmethod
    def axis_angle(axis: Vector3D, angle: float) -> Quaternion:
        v = axis.normalize()
        rad = radians(angle / 2)
        s = sin(rad)
        w = cos(rad)
        vs = v * s

        return Quaternion(w, vs)

    @staticmethod
    def identity() -> Quaternion:
        return Quaternion(1, Vector3D())

    def __mul__(self, other: Quaternion) -> Quaternion:
        t0 = (other.w * self.w - other.axis.x * self.axis.x - other.axis.y * self.axis.y - other.axis.z * self.axis.z)
        t1 = (other.w * self.axis.x + other.axis.x * self.w - other.axis.y * self.axis.z + other.axis.z * self.axis.y)
        t2 = (other.w * self.axis.y + other.axis.x * self.axis.z + other.axis.y * self.w - other.axis.z * self.axis.x)
        t3 = (other.w * self.axis.z - other.axis.x * self.axis.y + other.axis.y * self.axis.x + other.axis.z * self.w)
        return Quaternion(t0, Vector3D(x=t1, y=t2, z=t3))

    def __str__(self) -> str:
        return "({:.5f}, {:.5f}, {:.5f}, {:.5f})".format(self.w, self.axis.x, self.axis.y, self.axis.z)
