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
                    clip_result = plane.clip_triangle(triangle)
                    clipped_triangles.extend(clip_result)
                triangles = clipped_triangles
                clipped_triangles = []
            mesh.set_triangles(*triangles)
