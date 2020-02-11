from queue import Queue, Empty
from threading import Thread
from typing import List, Optional

from rendering.pipeline_step import PipelineStep
from scene.scene import Scene


class Pipeline:
    input_queue: Queue
    output_queue = Queue(maxsize=2)

    def __init__(self, steps: List[PipelineStep] = []):
        self.input_queue = self.output_queue
        if len(steps) == 0:
            return
        self.steps = steps

        for idx in range(len(steps)):
            step = steps[idx]
            if idx == 0:
                self.input_queue = step.input_queue
            else:
                steps[idx - 1].output_queue = step.input_queue
            step.output_queue = self.output_queue
            step.start()

    def stop(self):
        for step in self.steps:
            step.stop()

    def push_scene(self, scene: Scene):
        self.input_queue.put(scene)

    def pull_scene(self) -> Optional[Scene]:
        try:
            return self.output_queue.get_nowait()
        except Empty:
            return None
