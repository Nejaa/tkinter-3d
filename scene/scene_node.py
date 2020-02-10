from __future__ import annotations

from scene.entity import Entity


class SceneNode:
    def __init__(self, parent: SceneNode = None):
        self.parent = parent
        if parent is not None:
            parent.register_child(self)

        self.childs = []
        self.entities = []

    def add_entity(self, entity: Entity):
        self.entities.append(entity)

    def register_child(self, child:  SceneNode):
        self.childs.append(child)
