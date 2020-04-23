from geometry.camera import Camera
from rendering.pipeline_step import PipelineStep
from scene.scene import Scene


class ProjectionStep(PipelineStep):
    def __init__(self, camera: Camera):
        super().__init__()
        self.camera = camera

    def process_scene(self, scene: Scene):
        ent = scene.entities()
        mhs = [entity.geometry for entity in ent]
        for idx, mesh in enumerate(mhs):
            self.camera.project_mesh(mesh=mesh)
