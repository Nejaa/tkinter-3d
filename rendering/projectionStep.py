from geometry.camera import Camera
from rendering.pipeline_step import PipelineStep
from scene.scene import Scene


class ProjectionStep(PipelineStep):
    def __init__(self, camera: Camera):
        super().__init__()
        self.camera = camera
        self.step_name = "Projection"

    def process_scene(self, scene: Scene):
        self.camera.rebuild_projection_matrix()

        ent = scene.entities()
        mhs = [entity.geometry for entity in ent]
        for idx, mesh in enumerate(mhs):
            self.camera.project_mesh(mesh=mesh)
