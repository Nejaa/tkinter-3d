from geometry import Mesh, Vector


class Cube(Mesh):
    def __init__(self, center: Vector = Vector(), cube_size=10):
        origin = center - Vector(
            x=cube_size / 2,
            y=cube_size / 2,
            z=cube_size / 2,
        )
        base_vertices = {
            "A": Vector("A", 0, 0, 0).translate(origin),
            "B": Vector("B", 0, cube_size, 0).translate(origin),
            "C": Vector("C", cube_size, cube_size, 0).translate(origin),
            "D": Vector("D", cube_size, 0, 0).translate(origin),
            "E": Vector("E", 0, 0, cube_size).translate(origin),
            "F": Vector("F", 0, cube_size, cube_size).translate(origin),
            "G": Vector("G", cube_size, cube_size, cube_size).translate(origin),
            "H": Vector("H", cube_size, 0, cube_size).translate(origin),
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
        self.set_center(center)
