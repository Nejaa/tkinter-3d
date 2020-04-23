from rendering.pipeline_step import PipelineStep
from scene.scene import Scene


class WorldTransformStep(PipelineStep):
    def __init__(self):
        super().__init__()

    def process_scene(self, scene: Scene):
        scene.build_global_positions()
