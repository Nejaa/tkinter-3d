from tkinter import Canvas

from geometry.vector import Vector
from geometry.line import Line


class Triangle:
    def __init__(self, a: Vector, b: Vector, c: Vector):
        self.a = a  # unused but who knows
        self.b = b  # unused but who knows
        self.c = c  # unused but who knows
        self.ab = Line(self.a, self.b)
        self.bc = Line(self.b, self.c)
        self.ca = Line(self.c, self.a)

    def draw(self, canvas: Canvas):
        self.ab.draw(canvas)
        self.bc.draw(canvas)
        self.ca.draw(canvas)