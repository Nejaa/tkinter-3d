from geometry.mesh import Mesh
from geometry.vector import Vector


class Cube(Mesh):
    def __init__(self, origin: Vector = Vector(), cube_size=10):
        center = Vector(
            x=cube_size / 2,
            y=cube_size / 2,
            z=cube_size / 2,
        )

        vertices = {
            "A": Vector("A", 0, 0, 0) - center,
            "B": Vector("B", 0, cube_size, 0) - center,
            "C": Vector("C", cube_size, cube_size, 0) - center,
            "D": Vector("D", cube_size, 0, 0) - center,
            "E": Vector("E", 0, 0, cube_size) - center,
            "F": Vector("F", 0, cube_size, cube_size) - center,
            "G": Vector("G", cube_size, cube_size, cube_size) - center,
            "H": Vector("H", cube_size, 0, cube_size) - center,
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
