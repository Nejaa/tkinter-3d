from abc import ABC, abstractmethod
from queue import Queue
from typing import Optional

from scene.scene import Scene


class PipelineStep(ABC):
    output_queue: Queue = None
    running: bool = False

    def __init__(self):
        self.input_queue = Queue(maxsize=2)

    def fetch_scene(self) -> Scene:
        return self.input_queue.get(block=True, timeout=None)

    def send_scene(self, scene: Scene):
        if self.output_queue is None:
            return
        if self.output_queue.full():
            try:
                self.output_queue.get()  # discard one from head to make room; frame loss
            finally:
                pass
        try:
            self.output_queue.put_nowait(scene)
        finally:
            pass

    def run(self):
        self.running = True
        while self.running:
            scene = self.fetch_scene()
            self.process_scene(scene=scene)
            self.send_scene(scene=scene)

    @abstractmethod
    def process_scene(self, scene: Scene):
        pass
