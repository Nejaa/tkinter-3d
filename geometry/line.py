from tkinter import Canvas

from geometry import geometry_options
from custom_math.vector3d import Vector3D


class Line:
    def __init__(self, a: Vector3D, b: Vector3D):
        self.a = a
        self.b = b
