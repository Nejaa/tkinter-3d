from custom_math.matrix import Matrix
from custom_math.vector3d import Vector3D


def build_point_at_matrix(position: Vector3D, target: Vector3D, up: Vector3D) -> Matrix:
    # calculate forward
    forward = (target - position).normalize()

    # calculate up
    a = forward * up.dot(forward)
    up = (up - a).normalize()

    # calculate right
    right = up.cross(forward)

    return Matrix([
        [right.x, right.y, right.z, 0],
        [up.x, up.y, up.z, 0],
        [forward.x, forward.y, forward.z, 0],
        [position.x, position.y, position.z, 1]])


def build_look_at_matrix(position: Vector3D, target: Vector3D, up: Vector3D) -> Matrix:
    # calculate forward
    forward = (target - position).normalize()

    # calculate up
    a = forward * up.dot(forward)
    up = (up - a).normalize()

    # calculate right
    right = up.cross(forward)
    return Matrix([[right.x, up.x, forward.x, 0],
                   [right.y, up.y, forward.y, 0],
                   [right.z, up.z, forward.z, 0],
                   [-(position.dot(right)), -(position.dot(up)), -(position.dot(forward)), 1]])
