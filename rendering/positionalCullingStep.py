from geometry.camera import Camera
from rendering.pipeline_step import PipelineStep
from scene.scene import Scene


class PositionalCullingStep(PipelineStep):
    def __init__(self, camera: Camera):
        super().__init__()
        self.camera = camera
        self.step_name = "Positional Culling"

    def process_scene(self, scene: Scene):

        for entity in scene.entities():
            mesh = entity.geometry
            triangles = mesh.triangles
            final_triangles = []
            for triangle in triangles:
                if (triangle.a - self.camera.position).normalize().dot(self.camera.globalBearing) <= 0 or \
                        (triangle.b - self.camera.position).normalize().dot(self.camera.globalBearing) <= 0 or \
                        (triangle.c - self.camera.position).normalize().dot(self.camera.globalBearing) <= 0:
                    continue
                final_triangles.append(triangle)
            mesh.set_triangles(*final_triangles)
