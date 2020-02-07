from math import radians, pi, cos, sin

from geometry.vector import Vector
from geometry.quaternion import Quaternion


class Camera:
    def __init__(self, position: Vector, focal_length: float = 500):
        self.position = position.copy(label="camera")
        self.rotation = Quaternion.identity()
        self.bearing = Vector(z=1)
        self.view_port = Vector(label="view_port", z=focal_length)

    def translate(self, v: Vector):
        self.position.translate(v)

    def rotate(self, axis: Vector, angle: float):
        a = axis  # self.rotation.rotate(axis)
        rot = Quaternion.axis_angle(a, angle)
        self.bearing.move_to(rot.rotate(self.bearing))
        self.rotation *= rot

    def project(self, point: Vector, mesh_position: Vector):
        euler = self.rotation.euler_angles()
        cx = cos(euler.x)
        sx = sin(euler.x)
        cy = cos(euler.y)
        sy = sin(euler.y)
        cz = cos(euler.z)
        sz = sin(euler.z)

        delta = point + mesh_position - self.position

        if delta.dot(self.bearing) <= 1:
            point.visible = False
            return

        d_x = cy * (sz * delta.y + cz * delta.x) - sy * delta.z
        d_y = sx * (cy * delta.z + sy * (sz * delta.y + cz * delta.x)) + cx * (cz * delta.y - sz * delta.x)
        d_z = cx * (cy * delta.z + sy * (sz * delta.y + cz * delta.x)) - sx * (cz * delta.y - sz * delta.x)

        x = (self.view_port.z / d_z) * d_x
        y = (self.view_port.z / d_z) * d_y

        point.projection = Vector(point.label, x, -y)  # reverse y as the screen origin is top left
        point.visible = True

    def __str__(self):
        euler_angles = self.rotation.euler_angles()
        return "camera:\n" \
               "    position={}\n" \
               "    rotation_quat={}\n" \
               "    rotation_euler={}\n" \
               "    rotation_euler_deg={}\n" \
               "    bearing={}\n" \
               "    viewport offset={}".format(self.position, self.rotation, euler_angles, euler_angles.to_degree(),
                                               self.bearing, self.view_port)
