from tkinter import Canvas

from geometry import geometry_options
from geometry.vector import Vector


class Line:
    def __init__(self, a: Vector, b: Vector):
        self.a = a
        self.b = b

    def draw(self, canvas: Canvas):
        if self.a.visible & self.b.visible:
            canvas.create_line(self.a.projection.x, self.a.projection.y, self.b.projection.x, self.b.projection.y,
                               width=geometry_options.line_thickness)