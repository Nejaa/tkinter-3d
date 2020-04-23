from geometry.camera import Camera
from rendering.pipeline_step import PipelineStep
from rendering.renderer import Renderer
from scene.scene import Scene


class RenderingStep(PipelineStep):
    def __init__(self, renderer: Renderer):
        super().__init__()
        self.renderer = renderer

    def process_scene(self, scene: Scene):
        self.renderer.newScene = scene
