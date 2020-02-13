from abc import ABC, abstractmethod
from queue import Queue, Empty, Full
from threading import Thread
from typing import Optional

from scene.scene import Scene


class PipelineStep(ABC, Thread):
    input_queue = Queue(maxsize=1)
    output_queue: Queue = None
    running: bool = False

    def __init__(self):
        super().__init__()

    def fetch_scene(self) -> Scene:
        scene = None
        while scene is None:
            try:
                scene = self.input_queue.get(block=True, timeout=0.5)
            except Empty:
                pass

        return scene

    def send_scene(self, scene: Scene):
        if self.output_queue is None:
            return
        if self.output_queue.full():
            try:
                self.output_queue.get()  # discard one from head to make room; frame loss
            except Full:
                pass
        try:
            self.output_queue.put_nowait(scene)
        except Full:
            pass

    def run(self):
        self.running = True
        while self.running:
            scene = self.fetch_scene()
            self.process_scene(scene=scene)
            self.send_scene(scene=scene)

    def stop(self):
        self.running = False

    @abstractmethod
    def process_scene(self, scene: Scene):
        pass
