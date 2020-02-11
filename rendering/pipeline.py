from queue import Queue
from threading import Thread
from typing import List

from rendering.pipeline_step import PipelineStep


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
