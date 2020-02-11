from rendering.pipeline_step import PipelineStep
from scene.scene import Scene


class CollectorStep(PipelineStep):
    def __init__(self):
        super().__init__()

    def process_scene(self, scene: Scene):
        pass
