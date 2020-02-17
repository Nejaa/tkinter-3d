from math import cos, sin

from geometry.quaternion import Quaternion
from geometry.vector import Vector


class Camera:
    def __init__(self, position: Vector = Vector(), focal_length: float = 500, viewport_offset: Vector = Vector()):
        self.position = position.copy(label="camera")
        self.rotation = Quaternion.identity()
        self.bearing = Vector(z=1)
        self.bearing.projection = Vector(z=1)
        self.view_port = viewport_offset.copy(label="view_port")
        self.view_port.z = focal_length
        self.C = Vector(x=cos(0), y=cos(0), z=cos(0))
        self.S = Vector(x=sin(0), y=sin(0), z=sin(0))

    def translate(self, v: Vector, global_movement: bool = False):
        if not global_movement:
            v = self.rotation.rotate(v)

        self.position.translate(v)

    def rotate(self, axis: Vector, angle: float, global_rotation: bool = False):
        rot = Quaternion.axis_angle(axis=axis, angle=angle)

        if global_rotation:
            self.rotation = rot * self.rotation  # rotate over current camera rotation
        else:
            self.rotation = self.rotation * rot  # rotate under current camera rotation

        self.update_data()

    def update_data(self):
        self.bearing.projection.move_to(self.rotation.rotate(self.bearing))
        euler = self.rotation.euler_angles()
        self.C = Vector(x=cos(euler.x), y=cos(euler.y), z=cos(euler.z))
        self.S = Vector(x=sin(euler.x), y=sin(euler.y), z=sin(euler.z))

    def project(self, point: Vector, mesh_position: Vector):
        cx = self.C.x
        cy = self.C.y
        cz = self.C.z

        sx = self.S.x
        sy = self.S.y
        sz = self.S.z

        delta = point + mesh_position - self.position

        dot = delta.dot(self.bearing.projection)
        if dot <= 0:
            point.visible = False
            return

        d_x = cy * (sz * delta.y + cz * delta.x) - sy * delta.z
        d_y = sx * (cy * delta.z + sy * (sz * delta.y + cz * delta.x)) + cx * (cz * delta.y - sz * delta.x)
        d_z = cx * (cy * delta.z + sy * (sz * delta.y + cz * delta.x)) - sx * (cz * delta.y - sz * delta.x)

        x = (self.view_port.z / d_z) * d_x + self.view_port.x
        y = (-(self.view_port.z / d_z) * d_y) + self.view_port.y # reverse y as the screen origin is top left

        point.projection = Vector(point.label, x, y)
        point.projection.d = dot
        point.visible = True

    def __str__(self):
        euler_angles = self.rotation.euler_angles()
        return "camera:\n" \
               "    position={}\n" \
               "    rotation_quat={}\n" \
               "    rotation_euler={}\n" \
               "    bearing={}\n" \
               "    viewport offset={}".format(self.position, self.rotation, euler_angles.to_degree(),
                                               self.bearing.projection, self.view_port)
