from geometry.mesh import Mesh
from geometry.vector import Vector


class Plane(Mesh):
    def __init__(self, origin: Vector = Vector(), grid_size=10.0, length: int = 10):
        vertices = [[Vector(x=float(x*grid_size), y=float(y*grid_size)) for x in range(length)] for y in range(length)]

        trianglesList = []
        for y in range(len(vertices)-1):
            for x in range(len(vertices[y])):
                if x == 0:
                    continue  # skip first column
                # first triangle
                trianglesList.append(vertices[y][x])
                trianglesList.append(vertices[y][x - 1])
                trianglesList.append(vertices[y + 1][x - 1])

                # second triangle
                trianglesList.append(vertices[y][x])
                trianglesList.append(vertices[y + 1][x - 1])
                trianglesList.append(vertices[y + 1][x])

        super().__init__(*trianglesList)
        self.set_center(origin)
