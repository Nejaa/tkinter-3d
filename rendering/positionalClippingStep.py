from custom_math.plane import Plane
from geometry.camera import Camera
from rendering.pipeline_step import PipelineStep
from scene.scene import Scene


class PositionalClippingStep(PipelineStep):
    def __init__(self, camera: Camera):
        super().__init__()
        self.camera = camera
        self.step_name = "Positional Clipping"

    def process_scene(self, scene: Scene):

        bearing = self.camera.globalBearing.normalize()
        culling_plane = Plane(position=self.camera.position + bearing * 10,
                              normal=bearing)
        for entity in scene.entities():
            mesh = entity.geometry
            triangles = mesh.triangles
            clipped_triangles = []
            for triangle in triangles:
                clip_result = culling_plane.clip_triangle(triangle)
                clipped_triangles.extend(clip_result)
            mesh.set_triangles(*clipped_triangles)
