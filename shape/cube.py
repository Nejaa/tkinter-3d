from geometry.triangle import Triangle
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
            Triangle(a=vertices["A"],
                     b=vertices["B"],
                     c=vertices["D"],
                     ),
            Triangle(a=vertices["B"],
                     b=vertices["C"],
                     c=vertices["D"],
                     ),
            Triangle(a=vertices["D"],
                     b=vertices["C"],
                     c=vertices["H"],
                     ),
            Triangle(a=vertices["C"],
                     b=vertices["G"],
                     c=vertices["H"],
                     ),
            Triangle(a=vertices["H"],
                     b=vertices["G"],
                     c=vertices["E"],
                     ),
            Triangle(a=vertices["G"],
                     b=vertices["F"],
                     c=vertices["E"],
                     ),
            Triangle(a=vertices["E"],
                     b=vertices["F"],
                     c=vertices["A"],
                     ),
            Triangle(a=vertices["F"],
                     b=vertices["B"],
                     c=vertices["A"],
                     ),
            Triangle(a=vertices["E"],
                     b=vertices["A"],
                     c=vertices["H"],
                     ),
            Triangle(a=vertices["A"],
                     b=vertices["D"],
                     c=vertices["H"],
                     ),
            Triangle(a=vertices["B"],
                     b=vertices["F"],
                     c=vertices["C"],
                     ),
            Triangle(a=vertices["F"],
                     b=vertices["G"],
                     c=vertices["C"],
                     ),
        ]

        super().__init__(*triangles)
        self.set_center(origin)
