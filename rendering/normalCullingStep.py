from geometry.camera import Camera
from rendering.pipeline_step import PipelineStep
from scene.scene import Scene


class NormalCullingStep(PipelineStep):
    def __init__(self, camera: Camera):
        super().__init__()
        self.camera = camera

    def process_scene(self, scene: Scene):
        for entity in scene.entities():
            mesh = entity.geometry
            triangles = mesh.triangles
            final_triangles = []
            for triangle in triangles:
                triangle_n = triangle.normal()
                if triangle_n.dot((triangle.a - self.camera.position).normalize()) <= 0:
                    final_triangles.append(triangle)
            mesh.set_triangles(*final_triangles)
