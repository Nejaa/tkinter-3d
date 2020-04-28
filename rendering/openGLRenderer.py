from __future__ import annotations

import time
from datetime import timedelta
from tkinter import Canvas, Tk

from PIL.ImageTk import PhotoImage

from custom_math.vector3d import Vector3D
from geometry import geometry_options
from geometry.camera import Camera
from options import options
from rendering.renderer import Renderer
from scene.scene import Scene

import OpenGL


class OpenGLRenderer(Canvas, Renderer):
    def __init__(self, width: int, height: int, camera: Camera, **kwargs):
        Canvas.__init__(self, width=width, height=height, **kwargs)
        self.pack()

        self.width = width
        self.height = height
        self.windowCenter = Vector3D(x=width / 2, y=height / 2)

        self.frames = 0
        self.fps = 0
        self.inverted_y = False

        self.camera = camera
        camera.invert_y = False

        # start renderer
        self.after(ms=1000, func=self.fps_counter)
        self.after(ms=1, func=self.draw)

    def draw(self):
        if self.newScene is not None:
            self.curScene = self.newScene
            self.newScene = None

        if self.curScene is None:
            self.after(ms=10, func=self.draw)
            return

        t0 = time.time()
        self.delete("all")

        for entity in self.curScene.entities():
            mesh = entity.geometry
            # scale into view for openGL
            for vertex in mesh.vertices:
                vertex.x += 1
                vertex.x += 1
                vertex.x *= 0.5 * self.width
                vertex.y *= 0.5 * self.height

            for triangle in mesh.triangles:
                self.create_line(triangle.ab.a.x, triangle.ab.a.y,
                                 triangle.ab.b.x, triangle.ab.b.y,
                                 width=geometry_options.line_thickness)
                self.create_line(triangle.bc.a.x, triangle.bc.a.y,
                                 triangle.bc.b.x, triangle.bc.b.y,
                                 width=geometry_options.line_thickness)
                self.create_line(triangle.ca.a.x, triangle.ca.a.y,
                                 triangle.ca.b.x, triangle.ca.b.y,
                                 width=geometry_options.line_thickness)
                if options.debug and triangle.debugNormal is not None:
                    self.create_line(triangle.center.x, triangle.center.y,
                                     triangle.debugNormal.x, triangle.debugNormal.y,
                                     width=geometry_options.line_thickness)

            if options.debug:
                self.create_text(mesh.viewportPosition.x, mesh.viewportPosition.y,
                                 text="Center = {}\nRotation = {}".format(mesh.center, mesh.rotation))
                for vertex in mesh.vertices:
                    self.create_text(vertex.x, vertex.y, text=vertex.debug_txt)

        if options.draw_fps:
            self.create_text(20, 10, text=self.fps)

        if options.draw_crosshair:
            self.create_line(self.windowCenter.x, self.windowCenter.y - options.cross_hair_scale,
                             self.windowCenter.x, self.windowCenter.y + options.cross_hair_scale,
                             width=2)
            self.create_line(self.windowCenter.x - options.cross_hair_scale, self.windowCenter.y,
                             self.windowCenter.x + options.cross_hair_scale, self.windowCenter.y,
                             width=2)

        if options.debug:
            self.create_text(145, 40, text="{}".format(self.camera))

        print("rendering took {} ms\n".format((time.time() - t0) * 1000))

        self.frames += 1

        self.after(ms=1, func=self.draw)

    def fps_counter(self):
        self.fps = self.frames
        self.frames = 0
        self.after(ms=1000, func=self.fps_counter)