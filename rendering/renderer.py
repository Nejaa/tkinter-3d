from abc import ABC, abstractmethod

from scene.scene import Scene


class Renderer:
    curScene: Scene = None
    newScene: Scene = None
    width: int
    height: int

    def __init__(self):
        super().__init__()
