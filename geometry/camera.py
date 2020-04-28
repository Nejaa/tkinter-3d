from __future__ import annotations
from abc import abstractmethod, ABC
import enum
from math import cos, sin, tan, radians

from custom_math.matrix import Matrix
from custom_math.quaternion import Quaternion
from custom_math.vector3d import Vector3D
from geometry.mesh import Mesh
from options import options


class ProjectionMatrixBuilder(ABC):
    lerp_projection: bool

    @abstractmethod
    def build_matrix(self, camera: Camera) -> Matrix:
        pass


class PseudoPerspectiveMatrixBuilder(ProjectionMatrixBuilder):
    lerp_projection = True

    def build_matrix(self, camera: Camera) -> Matrix:
        itan = 1 / tan(radians(options.fov / 2))
        plane_delta = options.far_plane - options.close_plane
        return Matrix([
            [(options.height / options.width) * itan, 0, 0, 0.0],
            [0, itan, 0, 0],
            [0, 0, options.far_plane / plane_delta, 1],
            [0, 0, (-options.far_plane * options.close_plane) / plane_delta, 0]
        ])


class RealPerspectiveMatrixBuilder(ProjectionMatrixBuilder):
    lerp_projection = False

    def build_matrix(self, camera: Camera) -> Matrix:
        C = camera.C
        S = camera.S
        rx = Matrix(
            [
                [1, 0, 0, 0],
                [0, C.x, S.x, 0],
                [0, -S.x, C.x, 0],
                [0, 0, 0, 1],
            ]
        )

        ry = Matrix(
            [
                [C.y, 0, -S.y, 0],
                [0, 1, 0, 0],
                [S.y, 0, C.y, 0],
                [0, 0, 0, 1],
            ]
        )

        rz = Matrix(
            [
                [C.z, S.z, 0, 0],
                [-S.z, C.z, 0, 0],
                [0, 0, 1, 0],
                [0, 0, 0, 1],
            ]
        )

        return rx @ ry @ rz


class ProjectionType(enum.Enum):
    def __new__(cls, *args, **kwargs):
        value = len(cls.__members__) + 1
        obj = object.__new__(cls)
        obj._value_ = value
        return obj

    def __init__(self, builder: ProjectionMatrixBuilder):
        self.builder = builder
        self.lerp_projection = builder.lerp_projection

    def build_matrix(self, camera: Camera):
        return self.builder.build_matrix(camera)

    RealPerspective = RealPerspectiveMatrixBuilder()
    PseudoPerspective = PseudoPerspectiveMatrixBuilder()


class Camera:
    def __init__(self, position: Vector3D = Vector3D(), focal_length: float = 500,
                 viewport_offset: Vector3D = Vector3D(),
                 projection_type: ProjectionType = ProjectionType.RealPerspective,
                 debug=False, invert_y=False):
        self.debug = debug
        self.invert_y = invert_y

        self.projection_type = projection_type
        self.projection_matrix: Matrix = None

        self.position = position.copy(label="camera")
        self.rotation = Quaternion.identity()
        self.bearing = Vector3D(z=1)
        self.globalBearing = Vector3D(z=1)
        self.up = Vector3D(y=1)

        self.view_port = viewport_offset.copy(label="view_port")
        self.view_port.z = focal_length

        self.C = Vector3D(x=cos(0), y=cos(0), z=cos(0))
        self.S = Vector3D(x=sin(0), y=sin(0), z=sin(0))

        self.rebuild_projection_matrix()

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
        self.up = self.rotation.rotate(self.up)
        euler = self.rotation.euler_angles()
        self.C = Vector3D(x=cos(euler.x), y=cos(euler.y), z=cos(euler.z))
        self.S = Vector3D(x=sin(euler.x), y=sin(euler.y), z=sin(euler.z))

    def project_mesh(self, mesh: Mesh):
        mesh.viewportPosition = mesh.center.copy()
        self.project(mesh.viewportPosition)

        for triangle in mesh.triangles:
            if self.debug:
                tn = triangle.normal() * 5
                tn = tn.translate(triangle.center)
                self.project(tn)
                triangle.debugNormal = tn
            self.project(triangle.center)

        for vertex in mesh.vertices:
            self.project(vertex)

    def project(self, point: Vector3D):
        delta = self.position - point

        d = self.projection_matrix @ delta.to_matrix()
        dv = Vector3D(x=d[0][0], y=d[1][0], z=d[2][0])

        if self.invert_y:  # reverse y if needed
            dv.y = -dv.y

        if self.projection_type is ProjectionType.RealPerspective:
            dv.x = (self.view_port.z / dv.z) * dv.x + self.view_port.x
            dv.y = (self.view_port.z / dv.z) * dv.y + self.view_port.y
        else:
            if d[3][0] != 0.0:
                dv /= d[3][0]

        point.move_to(dv)

    def rebuild_projection_matrix(self):
        self.projection_matrix = self.projection_type.build_matrix(self)

    def __str__(self):
        euler_angles = self.rotation.euler_angles()
        return "camera:\n" \
               "    position={}\n" \
               "    rotation_quat={}\n" \
               "    rotation_euler={}\n" \
               "    bearing={}\n" \
               "    viewport offset={}".format(self.position, self.rotation, euler_angles.to_degree(),
                                               self.globalBearing, self.view_port)
