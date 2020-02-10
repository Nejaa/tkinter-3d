from typing import List

from scene.entity import Entity
from scene.scene_node import SceneNode


class Scene:
    def __init__(self):
        self.scene_root = SceneNode()

    def meshes(self):
        pass

    def entities(self):
        return self.entities_from_node(self.scene_root)

    def entities_from_node(self, node: SceneNode) -> List[Entity]:
        entities = node.entities
        for n in node.childs:
            entities.extend(self.entities_from_node(n))

        return entities
