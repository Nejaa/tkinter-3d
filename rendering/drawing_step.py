from tkinter import Canvas

from options import options
from rendering.pipeline_step import PipelineStep
from scene.scene import Scene


class DrawingStep(Canvas, PipelineStep):

    def run(self):
        self.after(100, self.work())

    def work(self):
        scene = self.fetch_scene()
        self.process_scene(scene=scene)
        self.after(1, self.work())

    def process_scene(self, scene: Scene):
        entities = scene.entities()
        meshes = [entity.geometry for entity in entities]

        self.delete("all")

        for idx, mesh in enumerate(meshes):
            mesh.draw(self, options.debug)

        h_width = options.width / 2
        h_height = options.height / 2
        self.create_line(h_width, h_height - options.cross_hair_scale,
                         h_width, h_height + options.cross_hair_scale,
                         width=2)
        self.create_line(h_width - options.cross_hair_scale, h_height,
                         h_width + options.cross_hair_scale, h_height,
                         width=2)
