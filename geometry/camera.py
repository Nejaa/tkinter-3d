from math import cos, sin

from custom_math.quaternion import Quaternion
from custom_math.vector3d import Vector3D
from geometry.mesh import Mesh


class Camera:
    def __init__(self, position: Vector3D = Vector3D(), focal_length: float = 500, viewport_offset: Vector3D = Vector3D()):
        self.position = position.copy(label="camera")
        self.rotation = Quaternion.identity()
        self.bearing = Vector3D(z=1)
        self.globalBearing = Vector3D(z=1)
        self.view_port = viewport_offset.copy(label="view_port")
        self.view_port.z = focal_length
        self.C = Vector3D(x=cos(0), y=cos(0), z=cos(0))
        self.S = Vector3D(x=sin(0), y=sin(0), z=sin(0))

    def translate(self, v: Vector3D, global_movement: bool = False):
        if not global_movement:
            v = self.rotation.rotate(v)

        self.position = self.position.translate(v)

    def rotate(self, axis: Vector3D, angle: float, global_rotation: bool = False):
        rot = Quaternion.axis_angle(axis=axis, angle=angle)

        if global_rotation:
            self.rotation = rot * self.rotation  # rotate over current camera rotation
        else:
            self.rotation = self.rotation * rot  # rotate under current camera rotation

        self.update_data()

    def update_data(self):
        self.globalBearing.move_to(self.rotation.rotate(self.bearing))
        euler = self.rotation.euler_angles()
        self.C = Vector3D(x=cos(euler.x), y=cos(euler.y), z=cos(euler.z))
        self.S = Vector3D(x=sin(euler.x), y=sin(euler.y), z=sin(euler.z))

    def project_mesh(self, mesh: Mesh):
        self.project(mesh.viewportPosition, mesh.center)
        for vertex in mesh.vertices:
            self.project(vertex, mesh.center)

    def project(self, point: Vector3D, mesh_position: Vector3D):
        cx = self.C.x
        cy = self.C.y
        cz = self.C.z

        sx = self.S.x
        sy = self.S.y
        sz = self.S.z

        delta = point + mesh_position - self.position

        dot = delta.dot(self.globalBearing)
        if dot <= 0:
            return

        d_x = cy * (sz * delta.y + cz * delta.x) - sy * delta.z
        d_y = sx * (cy * delta.z + sy * (sz * delta.y + cz * delta.x)) + cx * (cz * delta.y - sz * delta.x)
        d_z = cx * (cy * delta.z + sy * (sz * delta.y + cz * delta.x)) - sx * (cz * delta.y - sz * delta.x)

        x = (self.view_port.z / d_z) * d_x + self.view_port.x
        y = (-(self.view_port.z / d_z) * d_y) + self.view_port.y # reverse y as the screen origin is top left

        point.x = x
        point.y = y
        point.z = d_z

    def __str__(self):
        euler_angles = self.rotation.euler_angles()
        return "camera:\n" \
               "    position={}\n" \
               "    rotation_quat={}\n" \
               "    rotation_euler={}\n" \
               "    bearing={}\n" \
               "    viewport offset={}".format(self.position, self.rotation, euler_angles.to_degree(),
                                               self.globalBearing, self.view_port)
