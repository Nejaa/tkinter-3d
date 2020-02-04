from geometry.mesh import Mesh
from geometry.vector import Vector


class Cube(Mesh):
    def __init__(self, origin: Vector = Vector(), cube_size=10):
        center = Vector(
            x=cube_size / 2,
            y=cube_size / 2,
            z=cube_size / 2,
        )

        # o = origin - center

        base_vertices = {
            "A": Vector("A", 0, 0, 0) - center,
            "B": Vector("B", 0, cube_size, 0) - center,
            "C": Vector("C", cube_size, cube_size, 0) - center,
            "D": Vector("D", cube_size, 0, 0) - center,
            "E": Vector("E", 0, 0, cube_size) - center,
            "F": Vector("F", 0, cube_size, cube_size) - center,
            "G": Vector("G", cube_size, cube_size, cube_size) - center,
            "H": Vector("H", cube_size, 0, cube_size) - center,
        }

        vertices = [
            base_vertices["A"],
            base_vertices["B"],
            base_vertices["D"],

            base_vertices["B"],
            base_vertices["C"],
            base_vertices["D"],

            base_vertices["D"],
            base_vertices["C"],
            base_vertices["H"],

            base_vertices["C"],
            base_vertices["G"],
            base_vertices["H"],

            base_vertices["H"],
            base_vertices["G"],
            base_vertices["E"],

            base_vertices["G"],
            base_vertices["F"],
            base_vertices["E"],

            base_vertices["E"],
            base_vertices["F"],
            base_vertices["A"],

            base_vertices["F"],
            base_vertices["B"],
            base_vertices["A"],

            base_vertices["E"],
            base_vertices["A"],
            base_vertices["H"],

            base_vertices["A"],
            base_vertices["D"],
            base_vertices["H"],

            base_vertices["B"],
            base_vertices["F"],
            base_vertices["C"],

            base_vertices["F"],
            base_vertices["G"],
            base_vertices["C"],
        ]

        super().__init__(*vertices)
        self.set_center(origin)
