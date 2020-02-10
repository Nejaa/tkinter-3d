from abc import ABC, abstractmethod
from queue import Queue
from typing import Optional

from scene.scene import Scene


class PipelineStep(ABC):
    output_queue: Queue = None

    def __init__(self):
        self.input_queue = Queue()

    def fetch_scene(self) -> Scene:
        return self.input_queue.get(block=True, timeout=None)

    def send_scene(self, scene: Scene):
        if self.output_queue is None:
            return
        if self.output_queue.full():
            try:
                self.output_queue.get()
            finally:
                pass
        try:
            self.output_queue.put_nowait(scene)
        finally:
            pass

    @abstractmethod
    def process_scene(self, scene: Scene):
        pass
