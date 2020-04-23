from typing import List

from custom_math.plane import Plane
from custom_math.vector3d import Vector3D
from geometry.line import Line
from geometry.triangle import Triangle
from rendering.pipeline_step import PipelineStep
from rendering.renderer import Renderer
from scene.scene import Scene


class ScreenClippingStep(PipelineStep):
    def __init__(self, renderer: Renderer):
        super().__init__()
        self.width = renderer.width
        self.height = renderer.height

    def process_scene(self, scene: Scene):

        planes = [
            Plane(position=Vector3D(), normal=Vector3D.right()),  # left edge
            Plane(position=Vector3D(x=1), normal=Vector3D.down(screen_space=True)),  # up edge
            Plane(position=Vector3D(x=self.width), normal=Vector3D.left()),  # right edge
            Plane(position=Vector3D(y=self.height), normal=Vector3D.up(screen_space=True)),  # down edge
        ]

        for entity in scene.entities():
            mesh = entity.geometry
            triangles = mesh.triangles
            clipped_triangles = []
            for plane in planes:
                for triangle in triangles:
                    clip_result = self.clip_triangle(triangle, plane)
                    clipped_triangles.extend(clip_result)
                triangles = clipped_triangles
                clipped_triangles = []
            mesh.set_triangles(*triangles)

    def clip_triangle(self, triangle: Triangle, plane: Plane) -> List[Triangle]:

        inside_points = []
        outside_points = []

        if plane.dist(triangle.a) >= 0:
            inside_points.append(triangle.a)
        else:
            outside_points.append(triangle.a)
        if plane.dist(triangle.b) >= 0:
            inside_points.append(triangle.b)
        else:
            outside_points.append(triangle.b)
        if plane.dist(triangle.c) >= 0:
            inside_points.append(triangle.c)
        else:
            outside_points.append(triangle.c)

        inside_count = len(inside_points)
        if inside_count == 0:
            return []
        if inside_count == 3:
            return [triangle]

        outside_count = len(outside_points)
        if inside_count == 1 and outside_count == 2:
            return [
                Triangle(
                    a=inside_points[0],
                    b=plane.intersect(line=Line(a=inside_points[0], b=outside_points[0])),
                    c=plane.intersect(line=Line(a=inside_points[0], b=outside_points[1]))
                )
            ]

        if inside_count == 2 and outside_count == 1:
            t1 = Triangle(a=inside_points[0],
                          b=inside_points[1],
                          c=plane.intersect(line=Line(a=inside_points[0], b=outside_points[0])))

            t2 = Triangle(a=inside_points[1],
                          b=t1.c,
                          c=plane.intersect(line=Line(a=inside_points[1], b=outside_points[0])))
            return [
                t1,
                t2
            ]

        return []
