from geometry.camera import Camera
from rendering.BMPImage import BMPImage
from rendering.pipeline_step import PipelineStep
from rendering.renderer import Renderer
from scene.scene import Scene


class RenderingStep(PipelineStep):
    def __init__(self, renderer: Renderer):
        super().__init__()
        self.renderer = renderer

    def process_scene(self, scene: Scene):
        # image = BMPImage(width=self.renderer.width, height=self.renderer.height)
        # self.renderer.newScene = image.image
        if self.renderer.newScene is None:
            self.renderer.newScene = scene

