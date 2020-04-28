from abc import ABC, abstractmethod

from scene.scene import Scene


class Renderer:
    curScene = None
    newScene = None
    width: int
    height: int
    inverted_y: bool

    def __init__(self):
        super().__init__()
