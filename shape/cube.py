from geometry.mesh import Mesh
from custom_math.vector3d import Vector3D


class Cube(Mesh):
    def __init__(self, origin: Vector3D = Vector3D(), cube_size=10):
        center = Vector3D(
            x=cube_size / 2,
            y=cube_size / 2,
            z=cube_size / 2,
        )

        vertices = {
            "A": Vector3D("A", 0, 0, 0) - center,
            "B": Vector3D("B", 0, cube_size, 0) - center,
            "C": Vector3D("C", cube_size, cube_size, 0) - center,
            "D": Vector3D("D", cube_size, 0, 0) - center,
            "E": Vector3D("E", 0, 0, cube_size) - center,
            "F": Vector3D("F", 0, cube_size, cube_size) - center,
            "G": Vector3D("G", cube_size, cube_size, cube_size) - center,
            "H": Vector3D("H", cube_size, 0, cube_size) - center,
        }

        triangles = [
            vertices["A"],
            vertices["B"],
            vertices["D"],

            vertices["B"],
            vertices["C"],
            vertices["D"],

            vertices["D"],
            vertices["C"],
            vertices["H"],

            vertices["C"],
            vertices["G"],
            vertices["H"],

            vertices["H"],
            vertices["G"],
            vertices["E"],

            vertices["G"],
            vertices["F"],
            vertices["E"],

            vertices["E"],
            vertices["F"],
            vertices["A"],

            vertices["F"],
            vertices["B"],
            vertices["A"],

            vertices["E"],
            vertices["A"],
            vertices["H"],

            vertices["A"],
            vertices["D"],
            vertices["H"],

            vertices["B"],
            vertices["F"],
            vertices["C"],

            vertices["F"],
            vertices["G"],
            vertices["C"],
        ]

        super().__init__(*triangles)
        self.set_center(origin)
