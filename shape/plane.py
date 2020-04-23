from geometry.triangle import Triangle
from geometry.mesh import Mesh
from custom_math.vector3d import Vector3D


class Plane(Mesh):
    def __init__(self, origin: Vector3D = Vector3D(), grid_size=10.0, length: int = 10):
        vertices = [[Vector3D(x=float(x * grid_size), y=float(y * grid_size))
                     for x in range(length + 1)] for y in range(length + 1)]

        trianglesList = []
        for y in range(len(vertices) - 1):
            for x in range(len(vertices[y])):
                if x == 0:
                    continue  # skip first column
                # first triangle
                trianglesList.append(Triangle(a=vertices[x - 1][y],
                                              b=vertices[x][y],
                                              c=vertices[x - 1][y + 1],
                                              )),

                # second triangle
                trianglesList.append(Triangle(a=vertices[x][y],
                                              b=vertices[x][y + 1],
                                              c=vertices[x - 1][y + 1],
                                              ))

        super().__init__(*trianglesList)
        self.set_center(origin)
