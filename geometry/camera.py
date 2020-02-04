from math import radians, pi, cos, sin

from geometry.vector import Vector


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

    def project(self, point: Vector, mesh_position: Vector):
        cx = cos(self.rotation_rad.x)
        sx = sin(self.rotation_rad.x)
        cy = cos(self.rotation_rad.y)
        sy = sin(self.rotation_rad.y)
        cz = cos(self.rotation_rad.z)
        sz = sin(self.rotation_rad.z)

        delta = point + mesh_position - self.position

        if delta.dot(self.bearing) <= 0.0:
            point.visible = False
            return

        d_x = cy * (sz * delta.y + cz * delta.x) - sy * delta.z
        d_y = sx * (cy * delta.z + sy * (sz * delta.y + cz * delta.x)) + cx * (cz * delta.y - sz * delta.x)
        d_z = cx * (cy * delta.z + sy * (sz * delta.y + cz * delta.x)) - sx * (cz * delta.y - sz * delta.x)

        x = (self.view_port.z / d_z) * d_x
        y = (self.view_port.z / d_z) * d_y

        point.projection = Vector(point.label, x, y)
        point.visible = True

    def __str__(self):
        return "camera:\n" \
               "    position={}\n" \
               "    rotation={}\n" \
               "    rotation_rad={}\n" \
               "    bearing={}\n" \
               "    viewport offset={}".format(self.position, self.rotation, self.rotation_rad.copy() / pi,
                                               self.bearing,
                                               self.view_port)
